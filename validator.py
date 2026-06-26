"""
Image Validator
================
Validates uploaded images before running disease prediction.

Checks performed (in order):
  1. Format & basic integrity  → is it a real image?
  2. Size & resolution         → too small? too large?
  3. Blur detection            → Laplacian variance method
  4. Brightness check          → too dark or overexposed?
  5. Green channel dominance   → crude plant presence check
  6. Aspect ratio check        → valid leaf photo proportions

All checks are fast (CPU-only, no ML model required) so they
run before the expensive CNN inference.
"""

import io
import cv2
import numpy as np
from PIL import Image, UnidentifiedImageError


# ─────────────────────────────────────────────
# THRESHOLDS  (tune based on field testing)
# ─────────────────────────────────────────────

MIN_WIDTH         = 100       # pixels
MIN_HEIGHT        = 100
MAX_FILE_SIZE_MB  = 20        # reject enormous files
BLUR_THRESHOLD    = 80.0      # Laplacian variance; below = blurry
BRIGHTNESS_MIN    = 30        # 0-255; below = too dark
BRIGHTNESS_MAX    = 235       # above = overexposed
GREEN_RATIO_MIN   = 0.08      # fraction of pixels "green enough"
MIN_ASPECT_RATIO  = 0.25      # width/height; prevents panorama images
MAX_ASPECT_RATIO  = 4.0


class ValidationError(Exception):
    """Raised when an image fails a validation check."""
    def __init__(self, message: str, code: str, retake: bool = False):
        super().__init__(message)
        self.message = message
        self.code    = code
        self.retake  = retake   # True → ask user to retake photo


# ─────────────────────────────────────────────
# VALIDATION FUNCTIONS
# ─────────────────────────────────────────────

def check_file_integrity(file_bytes: bytes) -> Image.Image:
    """
    Verify the bytes are a valid, decodable image.
    Returns PIL Image on success, raises ValidationError on failure.
    """
    if len(file_bytes) == 0:
        raise ValidationError(
            "Empty file received. Please select an image.",
            code="EMPTY_FILE",
        )

    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise ValidationError(
            f"File too large ({size_mb:.1f} MB). Please compress the image and try again.",
            code="FILE_TOO_LARGE",
        )

    try:
        pil_img = Image.open(io.BytesIO(file_bytes))
        pil_img.verify()  # checks file is not truncated
        # Re-open after verify (verify() exhausts the stream)
        pil_img = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        return pil_img
    except UnidentifiedImageError:
        raise ValidationError(
            "Could not read the image. Please upload a JPG or PNG photo.",
            code="INVALID_FORMAT",
        )
    except Exception as e:
        raise ValidationError(
            f"Image appears corrupted: {e}",
            code="CORRUPTED_IMAGE",
        )


def check_resolution(pil_img: Image.Image):
    """Reject images that are too small to contain useful leaf detail."""
    w, h = pil_img.size
    if w < MIN_WIDTH or h < MIN_HEIGHT:
        raise ValidationError(
            f"Image is too small ({w}×{h}px). Please take a clearer, closer photo.",
            code="TOO_SMALL",
            retake=True,
        )
    ar = w / h
    if ar < MIN_ASPECT_RATIO or ar > MAX_ASPECT_RATIO:
        raise ValidationError(
            "Unusual image shape. Please take a standard portrait or landscape photo.",
            code="BAD_ASPECT_RATIO",
            retake=True,
        )


def check_blur(cv_img: np.ndarray) -> float:
    """
    Blur detection using Laplacian variance.

    The Laplacian operator detects edges. A sharp image has strong
    edges (high variance). A blurry image has soft edges (low variance).

    Returns the variance score (higher = sharper).
    """
    gray     = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()

    if variance < BLUR_THRESHOLD:
        raise ValidationError(
            f"Image is too blurry (sharpness: {variance:.0f}). "
            "Please hold your camera steady and retake the photo in good light.",
            code="IMAGE_BLURRY",
            retake=True,
        )
    return variance


def check_brightness(cv_img: np.ndarray) -> float:
    """
    Check average brightness of the image.
    Too dark → user may be indoors without light.
    Too bright → overexposed, details washed out.
    """
    gray       = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    brightness = float(np.mean(gray))

    if brightness < BRIGHTNESS_MIN:
        raise ValidationError(
            "Image is too dark. Please take the photo in natural daylight.",
            code="TOO_DARK",
            retake=True,
        )
    if brightness > BRIGHTNESS_MAX:
        raise ValidationError(
            "Image is overexposed (too bright). Move to a shaded area and retake.",
            code="OVEREXPOSED",
            retake=True,
        )
    return brightness


def check_plant_presence(cv_img: np.ndarray) -> float:
    """
    Lightweight 'is there a green plant in this image?' check.

    We convert to HSV and count pixels that fall in the green
    hue range (35–85° in OpenCV's 0–179° scale).
    This catches clearly non-plant images (solid walls, soil only,
    blue sky, people, objects).

    Limitation: diseased/yellowed leaves may have low green ratio.
    We use a LOW threshold (8%) to only reject obviously wrong images.

    Returns the fraction of green pixels.
    """
    hsv         = cv2.cvtColor(cv_img, cv2.COLOR_BGR2HSV)
    lower_green = np.array([25,  30,  30])   # HSV lower bound
    upper_green = np.array([95, 255, 255])   # HSV upper bound
    mask        = cv2.inRange(hsv, lower_green, upper_green)
    green_ratio = np.sum(mask > 0) / mask.size

    if green_ratio < GREEN_RATIO_MIN:
        raise ValidationError(
            "No plant detected in the image. Please take a close-up photo of a plant leaf.",
            code="NO_PLANT_DETECTED",
            retake=False,  # Not a retake issue — wrong subject
        )
    return green_ratio


# ─────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────

def validate_image(file_bytes: bytes) -> tuple[np.ndarray, dict]:
    """
    Run all validation checks on raw image bytes.

    Returns:
        (cv2_image, metadata_dict)  on success
    Raises:
        ValidationError             on any check failure
    """
    # 1. Decode
    pil_img = check_file_integrity(file_bytes)

    # 2. Resolution
    check_resolution(pil_img)

    # 3. Convert PIL → OpenCV (RGB → BGR)
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # 4. Blur
    sharpness = check_blur(cv_img)

    # 5. Brightness
    brightness = check_brightness(cv_img)

    # 6. Plant presence
    green_ratio = check_plant_presence(cv_img)

    metadata = {
        "width"       : pil_img.size[0],
        "height"      : pil_img.size[1],
        "sharpness"   : round(sharpness, 1),
        "brightness"  : round(brightness, 1),
        "green_ratio" : round(green_ratio * 100, 1),   # as percentage
    }

    return cv_img, metadata


def preprocess_for_model(cv_img: np.ndarray, target_size=(160, 160)) -> np.ndarray:
    """
    Resize and prepare a validated OpenCV image for model inference.
    NOTE: No /255 normalization here — EfficientNetB4 has an internal
    Rescaling layer that handles this. Dividing here too would double-scale
    the image and break predictions.
    """
    resized   = cv2.resize(cv_img, target_size, interpolation=cv2.INTER_AREA)
    rgb       = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    batched   = np.expand_dims(rgb.astype(np.float32), axis=0)
    return batched