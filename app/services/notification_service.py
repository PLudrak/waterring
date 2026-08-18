import os

import httpx
from dotenv import load_dotenv
from app.services.date_service import WateringStatus, get_plants_by_watering_status

load_dotenv()


def send_discord_notification(message: str):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")

    if not webhook_url:
        raise ValueError("DISCORD_WEBHOOK_URL is not set")

    response = httpx.post(
        webhook_url,
        json={"content": message},
        timeout=10,
    )

    response.raise_for_status()


def create_notification_content(plants_by_status):
    plants_critical = plants_by_status[WateringStatus.CRITICAL]
    plants_to_water = plants_by_status[WateringStatus.ALERT]
    message = "Hello @everyone!\n\n"

    if plants_critical:
        message += "🍂 Plants that have missed a watering:\n"

        for plant in plants_critical:
            message += f"● {plant.name}\n"

    if plants_to_water:
        message += "\n 🍀 Plants to water today:\n"

        for plant in plants_to_water:
            message += f"● {plant.name}\n"

    return message


def send_notification(db):
    plants_statuses = get_plants_by_watering_status(db)
    message = create_notification_content(plants_statuses)

    send_discord_notification(message)
