import os

import httpx
from dotenv import load_dotenv

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
