from pathlib import Path
from uuid import uuid4
from io import BytesIO

from fastapi import HTTPException, UploadFile
from PIL import Image

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_IMAGE_SIZE = 5 * 1024 * 1024

ALLOWED_FORMATS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}


async def upload_plant_image(image: UploadFile | None = None) -> str | None:
    if image is None or not image.filename:
        return None

    data = await image.read()

    if len(data) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400, detail="Image is too large, Maximum size is 5 MB."
        )

    try:
        pil_image = Image.open(BytesIO(data))
        pil_image.verify()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    image_format = pil_image.format

    if image_format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=400, detail="Unsuported image format.")

    extension = ALLOWED_FORMATS[image_format]
    filename = f"{uuid4()}{extension}"

    image_path = UPLOAD_DIR / "plants" / filename
    image_path.parent.mkdir(parents=True, exist_ok=True)

    image_path.write_bytes(data)

    return f"plants/{filename}"


async def update_plant_image(
    image: UploadFile | None = None, old_image_path: str | None = None
) -> str | None:
    new_image_path = await upload_plant_image(image)

    if new_image_path is None:
        return old_image_path

    if old_image_path:
        old_path = UPLOAD_DIR / old_image_path

        if old_path.exists():
            old_path.unlink()

    return new_image_path
