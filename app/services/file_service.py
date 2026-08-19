from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads/plants")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def upload_plant_image(image: UploadFile | None = None):
    if image and image.filename:
        extension = Path(image.filename).suffix.lower()
        filename = f"{uuid4()}{extension}"

        file_path = UPLOAD_DIR / filename

        with file_path.open("wb") as buffer:
            buffer.write(image.file.read())
        image_path = f"plants/{filename}"
        return image_path
