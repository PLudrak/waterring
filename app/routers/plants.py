from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
from app.core.templates import templates
from app.database import get_db
from app.models import Plant
from app.services.plant_service import parse_watering_range

router = APIRouter()


@router.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    plants = db.query(Plant).all()
    return templates.TemplateResponse(
        request, "index.html", {"request": request, "plants": plants}
    )


@router.post("/plants")
def create_plant(
    name: str = Form(...),
    watering_range: str = Form(...),
    db: Session = Depends(get_db),
):
    watering_interval_min, watering_interval_max = parse_watering_range(watering_range)
    plant = Plant(
        name=name,
        watering_interval_min=watering_interval_min,
        watering_interval_max=watering_interval_max,
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


@router.get("/manage-plants")
def manage_plants(
    request: Request, edit: int | None = None, db: Session = Depends(get_db)
):
    plants = db.query(Plant).all()

    return templates.TemplateResponse(
        request,
        "manage_plants.html",
        {"request": request, "plants": plants, "edit_id": edit},
    )


@router.post("/plants/{plant_id}/edit")
async def update_plant(plant_id: int, request: Request, db: Session = Depends(get_db)):
    plant = db.query(Plant).filter(Plant.id == plant_id).first()

    if not plant:
        raise HTTPException(status_code=404, detail="Plant not found")

    form = await request.form()

    plant.name = form["name"]
    plant.watering_min_days = int(form["watering_interval_min"])
    plant.watering_max_days = int(form["watering_interval_max"])

    db.commit()

    return RedirectResponse("/manage-plants", status_code=303)
