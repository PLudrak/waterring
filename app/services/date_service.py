from datetime import datetime, timezone
from app.models import Plant
from app.services.plant_service import get_all_plants
from enum import Enum


class WateringStatus(str, Enum):
    OK = "ok"
    ALERT = "alert"
    CRITICAL = "critical"


def days_since_watered(last_watered_at: datetime) -> int:
    now = datetime.now(timezone.utc)
    return (now.date() - last_watered_at.date()).days


def watering_text(days_since_watered) -> str:
    if days_since_watered == 0:
        return "Today"
    elif days_since_watered == 1:
        return "Yesterday"
    else:
        return f"{days_since_watered} days ago"


def watering_status(days_since, days_max, days_min):
    if days_since < days_min:
        return "ok"
    elif days_since < days_max:
        return "alert"
    else:
        return "critical"


def get_all_plants_info(db):
    plants = get_all_plants(db)

    for plant in plants:
        days_since = days_since_watered(plant.last_watered_at)
        plant.watered_label = watering_text(days_since)
        plant.status = watering_status(
            days_since, plant.watering_interval_max, plant.watering_interval_min
        )
        plant.status_description = watering_status_desciription(plant.status)
    return plants


def watering_status_desciription(status):
    if status == WateringStatus.ALERT:
        return "🥀💧 Needs water"
    if status == WateringStatus.CRITICAL:
        return "🍂 Needs urgent watering!"
    else:
        return "🌻 Ok"


def get_plants_by_watering_status(db):
    plants = get_all_plants_info(db)
    plants_watered = []
    plants_to_water = []
    plants_critical = []
    for plant in plants:
        if plant.status == WateringStatus.CRITICAL:
            plants_critical.append(plant)
        elif plant.status == WateringStatus.ALERT:
            plants_to_water.append(plant)
        else:
            plants_watered.append(plant)
    for plant in plants_critical:
        print(plant.name)
    return {
        "watered": plants_watered,
        "alert": plants_to_water,
        "critical": plants_critical,
    }
