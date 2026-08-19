from app.models import Plant
from app.database import SessionLocal
from fastapi import HTTPException
from datetime import datetime, timezone
from sqlalchemy.orm import Session


def parse_watering_range(value: str) -> tuple:
    if not value or value.strip() == "":
        return 6, 8
    if "-" in value:
        parts = value.split("-")
        parts_int = list(map(int, parts))
        min_days = min(parts_int)
        max_days = max(parts_int)
    else:
        min_days = max_days = int(value)

    return min_days, max_days


def create_plant(db, name: str, watering_interval):

    watering_interval_min, watering_interval_max = parse_watering_range(
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


def water_plant(plant_id: int, db: Session):
    plant = db.query(Plant).get(plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")

    plant.last_watered_at = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    db.commit()


def update_plant(
    db: Session,
    plant_id: int,
    name: str,
    watering_min_days: int,
    watering_max_days: int,
    last_watered_at: datetime,
):
    plant = db.get(Plant, plant_id)

    if plant is None:
        raise HTTPException(
            status_code=404,
            detail="Plant not found",
        )

    plant.name = name
    plant.watering_interval_min = watering_min_days
    plant.watering_interval_max = watering_max_days
    plant.last_watered_at = last_watered_at

    db.commit()

    return plant


def get_all_plants(db):
    plants = db.query(Plant).all()

    return plants
