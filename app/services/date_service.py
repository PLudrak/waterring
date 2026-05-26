from datetime import datetime


def days_since_watered(last_watered_at: datetime) -> int:
    delta = datetime.utcnow() - last_watered_at
    return delta.days


def watering_text(days_since_watered) -> str:
    if days_since_watered == 0:
        return "Today"
    elif days_since_watered == 1:
        return "Yesterday"
    else:
        return f"{days_since_watered} days ago"


def watering_status(days_since, days_max, days_min):
    if days_since < days_min:
        return "🟢 Good"
    elif days_since < days_max:
        return "🟡 Water me!"
    else:
        return "🔴 Water me!!!"
