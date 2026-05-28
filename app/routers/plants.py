from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.templates import templates
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

    plant.last_watered_at = datetime.now(timezone.utc).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

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
    plant.last_watered_at = datetime.fromisoformat(form["last_watered"]).replace(
        tzinfo=timezone.utc
    )
    db.commit()

    return RedirectResponse("/manage-plants", status_code=303)
