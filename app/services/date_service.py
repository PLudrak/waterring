from datetime import datetime, timezone
from app.models import Plant


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
        return "🟢 Good"
    elif days_since < days_max:
        return "🟡 Water me!"
    else:
        return "🔴 Water me!!!"


def get_all_plants_description(db):
    plants = db.query(Plant).all()

    for plant in plants:
        days_since = days_since_watered(plant.last_watered_at)
        plant.watered_label = watering_text(days_since)
        plant.status = watering_status(
            days_since, plant.watering_interval_max, plant.watering_interval_min
        )
    return plants
