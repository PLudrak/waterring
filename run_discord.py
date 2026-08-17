from app.services.notification_service import send_discord_notification

if __name__ == "__main__":
    send_discord_notification("@everyone 🌱 Test powiadomienia z WaterRing!")
