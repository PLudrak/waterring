from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from apscheduler.schedulers.background import BackgroundScheduler

from app.database import Base, engine, get_db
from app.models import Plant
from app.routers import plants

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")

app.include_router(plants.router)


@app.get("/")
def home(request: Request, db: Session = Depends(get_db)):
    plants = db.query(Plant).all()
    return templates.TemplateResponse(
        request, "index.html", {"request": request, "plants": plants}
    )
