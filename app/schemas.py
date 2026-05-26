from pydantic import BaseModel
from datetime import datetime


class PlantCreate(BaseModel):
    name: str
    watering_interval_min: int
    watering_interval_max: int


class PlantResponse(BaseModel):
    id: int
    name: str
    watering_interval_min: int
    watering_interval_max: int
    last_watered_at: datetime

    class Config:
        from_attributes = True
