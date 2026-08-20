from fastapi import HTTPException, UploadFile
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.services.file_service import upload_plant_image, update_plant_image
from app.models import Plant
from app.database import SessionLocal


def parse_watering_range(value: str | None) -> tuple:
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


def create_plant(
    db: Session,
    name: str,
    watering_interval: str | None,
    image: UploadFile | None = None,
):

    watering_interval_min, watering_interval_max = parse_watering_range(
        watering_interval
    )
    image_path = None
    if image:
        image_path = upload_plant_image(image)

    plant = Plant(
        name=name,
        watering_interval_min=watering_interval_min,
        watering_interval_max=watering_interval_max,
        image_path=image_path,
    )

    db.add(plant)
    db.commit()
    db.refresh(plant)
    return plant


def water_plant(plant_id: int, db: Session):
    plant = db.query(Plant).get(plant_id)
    if plant is None:
        raise HTTPException(status_code=404, detail="Plant not found")

    plant.last_watered_at = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    db.commit()


async def update_plant(
    db: Session,
    plant_id: int,
    name: str,
    watering_min_days: int,
    watering_max_days: int,
    last_watered_at: datetime,
    image: UploadFile | None = None,
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
    if image and image.filename:
        plant.image_path = await update_plant_image(
            image=image, old_image_path=plant.image_path
        )
    db.commit()
    db.refresh(plant)
    return plant


def get_all_plants(db):
    plants = db.query(Plant).all()

    return plants
