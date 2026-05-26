from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.database import get_db
from app.models import Plant

router = APIRouter()


@router.post("/plants")
def create_plant(
    name: str = Form(...),
    watering_interval_min: int = Form(...),
    watering_interval_max: int = Form(...),
    db: Session = Depends(get_db),
):
    plant = Plant(
        name=name,
        watering_interval_max=watering_interval_max,
        watering_interval_min=watering_interval_min,
    )

    db.add(plant)
    db.commit()

    return RedirectResponse("/", status_code=303)


@router.post("/plants/{plant_id}/water")
def water_plant(plant_id: int, db: Session = Depends(get_db)):

    plant = db.query(Plant).get(plant_id)

    plant.last_watered_at = datetime.utcnow()

    db.commit()

    return RedirectResponse("/", status_code=303)
