from app.services.notification_service import send_notification
from app.database import SessionLocal


def main():
    db = SessionLocal()

    try:
        send_notification(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
