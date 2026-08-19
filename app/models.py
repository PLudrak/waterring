from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from .database import Base


class Plant(Base):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)
    watering_interval_max: Mapped[int] = mapped_column(default=3)
    watering_interval_min: Mapped[int] = mapped_column(default=3)

    last_watered_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    info: Mapped[str] = mapped_column(default="")
    place: Mapped[str] = mapped_column(default="")

    image_path: Mapped[str] = mapped_column(String, nullable=True)


class Place(Base):
    __tablename__ = "places"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    room: Mapped[str] = mapped_column()
