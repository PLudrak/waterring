from pathlib import Path
from uuid import uuid4
from io import BytesIO

from fastapi import HTTPException, UploadFile
from PIL import Image

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_IMAGE_DIMENSIONS = (512, 512)

ALLOWED_FORMATS = {"JPEG": ".jpg", "PNG": ".png", "WEBP": ".webp"}


async def upload_plant_image(image: UploadFile | None = None) -> str | None:
    if image is None or not image.filename:
        return None

    data = await validate_image(image)
    resized_data = resize_image(data)

    filename = f"{uuid4()}.jpg"

    image_path = UPLOAD_DIR / "plants" / filename
    image_path.parent.mkdir(parents=True, exist_ok=True)

    image_path.write_bytes(resized_data)

    return f"plants/{filename}"


async def validate_image(image: UploadFile) -> bytes:
    data = await image.read()

    if len(data) > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="Image is too lareg, maximum size is 5 MB.",
        )
    try:
        pil_image = Image.open(BytesIO(data))
        pil_image.verify()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    if pil_image.format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=400, detail="Unsuported image format.")

    return data


def resize_image(data: bytes) -> bytes:
    image = Image.open(BytesIO(data))

    image.thumbnail(MAX_IMAGE_DIMENSIONS, Image.Resampling.LANCZOS)

    if image.mode in ("RGBA", "LA", "P"):
        background = Image.new("RGB", image.size, "white")

        if image.mode == "P":
            image = image.convert("RGBA")

        background.paste(
            image,
            mask=image.getchannel("A"),
        )

        image = background
    else:
        image = image.convert("RGB")

    output = BytesIO()

    image.save(output, format="JPEG", quality=85, optimization=True)
    return output.getvalue()


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
