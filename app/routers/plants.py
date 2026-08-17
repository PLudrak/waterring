from fastapi import APIRouter, Depends, Form, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.templates import templates
from app.services.date_service import get_all_plants_info, get_plants_by_watering_status
from app.database import get_db
from app.models import Plant
from app.services.plant_service import (
    water_plant,
    create_plant,
    get_all_plants,
    update_plant,
)

router = APIRouter()


@router.get("/")
def home_endpoint(request: Request, db: Session = Depends(get_db)):
    plants = get_all_plants_info(db)
    get_plants_by_watering_status(db)
    return templates.TemplateResponse(
        request, "index.html", {"request": request, "plants": plants}
    )


@router.post("/plants")
def create_plant_endpoint(
    name: str = Form(...),
    watering_range: str | None = Form(None),
    db: Session = Depends(get_db),
):
    create_plant(db, name, watering_range)

    return RedirectResponse("/", status_code=303)


@router.post("/plants/{plant_id}/water")
def water_plant_endpoint(plant_id: int, db: Session = Depends(get_db)):

    water_plant(plant_id, db)

    return RedirectResponse("/", status_code=303)


@router.get("/manage-plants")
def manage_plants(
    request: Request, edit: int | None = None, db: Session = Depends(get_db)
):
    plants = get_all_plants(db)
    return templates.TemplateResponse(
        request,
        "manage_plants.html",
        {"request": request, "plants": plants, "edit_id": edit},
    )


@router.post("/plants/{plant_id}/edit")
async def update_plant_endpoint(
    plant_id: int, request: Request, db: Session = Depends(get_db)
):

    form = await request.form()

    update_plant(
        db=db,
        plant_id=plant_id,
        name=str(form["name"]),
        watering_min_days=int(str(form["watering_interval_min"])),
        watering_max_days=int(str(form["watering_interval_max"])),
        last_watered_at=datetime.fromisoformat(str(form["last_watered"])).replace(
            tzinfo=timezone.utc
        ),
    )

    return RedirectResponse("/manage-plants", status_code=303)


@router.get("/manage-places")
def manage_places(request: Request, db: Session = Depends(get_db)):
    plants = get_all_plants(db)

    return templates.TemplateResponse(
        request,
        "manage_places.html",
        {"request": request, "plants": plants},
    )
