from fastapi import (
    APIRouter,
    Depends,
    Form,
    Request,
    HTTPException,
    File,
    UploadFile,
    Form,
)
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.core.templates import templates
from app.services.date_service import get_all_plants_info
from app.database import get_db
from app.models import Plant
from app.services.notification_service import send_notification
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
    return templates.TemplateResponse(
        request, "index.html", {"request": request, "plants": plants}
    )


@router.get("/notify")
def notify_endpoint(request: Request, db: Session = Depends(get_db)):
    send_notification(db)
    return RedirectResponse("/", status_code=303)


@router.post("/plants")
def create_plant_endpoint(
    name: str = Form(...),
    watering_range: str | None = Form(None),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    create_plant(db, name, watering_range, image)

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
    plant_id: int,
    name: str = Form(...),
    watering_min_days: int = Form(...),
    watering_max_days: int = Form(...),
    last_watered: str = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):

    if not isinstance(image, UploadFile):
        image = None

    await update_plant(
        db=db,
        plant_id=plant_id,
        name=name,
        watering_min_days=watering_min_days,
        watering_max_days=watering_max_days,
        last_watered_at=datetime.fromisoformat(last_watered).replace(
            tzinfo=timezone.utc
        ),
        image=image,
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
