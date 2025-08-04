"""OCR utilities for screen text extraction using pytesseract and Pillow."""
from __future__ import annotations

from typing import Optional, Tuple

from PIL import Image, ImageGrab
import pytesseract

def capture_region(region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
    """Capture a screenshot of the given region.

    Args:
        region: Optional bounding box ``(left, top, right, bottom)``.
    Returns:
        PIL Image containing the screenshot.
    """
    return ImageGrab.grab(bbox=region)

def ocr_image(image: Image.Image, lang: str = "eng") -> str:
    """Extract text from a PIL image using Tesseract.

    Args:
        image: Image to perform OCR on.
        lang: Language for Tesseract (default English).
    Returns:
        Extracted text as a string.
    """
    return pytesseract.image_to_string(image, lang=lang)

def ocr_screen(region: Optional[Tuple[int, int, int, int]] = None, lang: str = "eng") -> str:
    """Capture a region of the screen and perform OCR on it."""
    image = capture_region(region)
    return ocr_image(image, lang=lang)
