import io
from PIL import Image, ImageOps
from app.core.exceptions import ValidationException
from app.core.config import settings

def validate_and_preprocess_image(image_bytes: bytes, filename: str) -> Image.Image:
    """
    Validates uploaded image file size, magic bytes, dimensions, and sanitizes format.
    """
    # 1. Size check
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise ValidationException(
            message=f"Image size exceeds maximum allowed limit of {settings.MAX_UPLOAD_SIZE_MB}MB",
            details={"file_size_mb": round(size_mb, 2)}
        )
    
    # 2. Extension check
    ext = filename.split(".")[-1].lower() if "." in filename else ""
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        raise ValidationException(
            message=f"Unsupported file extension '{ext}'. Allowed extensions: {', '.join(settings.ALLOWED_IMAGE_EXTENSIONS)}",
            details={"allowed": settings.ALLOWED_IMAGE_EXTENSIONS}
        )

    # 3. Pillow decode and verify
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()  # Verifies integrity without loading full raster
        # Re-open after verify()
        image = Image.open(io.BytesIO(image_bytes))
        image = ImageOps.exif_transpose(image)  # Correct orientation
    except Exception as e:
        raise ValidationException(
            message="Corrupted or invalid image file. Could not decode image.",
            details={"error": str(e)}
        )

    # 4. Dimension check
    width, height = image.size
    if width < 50 or height < 50:
        raise ValidationException(
            message="Image dimensions too small for reliable diagnosis. Minimum 50x50 pixels required.",
            details={"width": width, "height": height}
        )
    if width > 10000 or height > 10000:
        raise ValidationException(
            message="Image dimensions excessively large. Maximum 10000x10000 pixels.",
            details={"width": width, "height": height}
        )

    return image
