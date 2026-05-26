from app.models import Plant
from app.database import SessionLocal


def parse_watering_range(value: str) -> tuple:
    if "-" in value:
        parts = value.split("-")
        parts_int = list(map(int, parts))
        min_days = min(parts_int)
        max_days = max(parts_int)
    else:
        min_days = max_days = int(value)

    return min_days, max_days


def create_plant(db, name: str, watering_interval):

    watering_interval_max, watering_interval_min = parse_watering_range(
        watering_interval
    )

    plant = Plant(
        name=name,
        watering_interval_min=watering_interval_min,
        watering_interval_max=watering_interval_max,
    )

    db.add(plant)
    db.commit()

    return plant
