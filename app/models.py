from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from .database import Base


class Plant(Base):
    __tablename__ = "plants"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    watering_interval_max = Column(Integer, default=3)
    watering_interval_min = Column(Integer, default=3)

    last_watered_at = Column(DateTime, default=datetime.utcnow)
    info = Column(String, default="")
    place = Column(String, default="")
