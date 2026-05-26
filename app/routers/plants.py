from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from app.templates import templates
from app.services.date_service import days_since_watered, watering_text, watering_status
from app.database import get_db
from app.models import Plant
from app.services.plant_service import parse_watering_range, create_plant

router = APIRouter()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    plants = db.query(Plant).all()

    for plant in plants:
        days_since = days_since_watered(plant.last_watered_at)
        plant.watered_label = watering_text(days_since)
        plant.status = watering_status(
            days_since, plant.watering_interval_max, plant.watering_interval_min
        )
    return templates.TemplateResponse(
        request, "index.html", {"request": request, "plants": plants}
    )


@router.post("/plants")
def create_plant_endpoint(
    name: str = Form(...),
    watering_range: str = Form(...),
    db: Session = Depends(get_db),
):
    plant = create_plant(db, name, watering_range)

    db.add(plant)
    db.commit()

    return RedirectResponse("/", status_code=303)


@router.post("/plants/{plant_id}/water")
def water_plant(plant_id: int, db: Session = Depends(get_db)):

    plant = db.query(Plant).get(plant_id)

    plant.last_watered_at = datetime.utcnow()

    db.commit()

    return RedirectResponse("/", status_code=303)
