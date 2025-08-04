"""Utility functions for locating images on the screen using OpenCV."""
from __future__ import annotations

from typing import Optional, Tuple

import cv2
import numpy as np
import pyautogui


def locate_on_screen(template_path: str, confidence: float = 0.8) -> Optional[Tuple[int, int]]:
    """Find the given template image on the current screen.

    Args:
        template_path: Path to the template image to search for.
        confidence: Matching threshold between 0 and 1.
    Returns:
        Top-left coordinates of the best match if found, otherwise ``None``.
    """
    screenshot = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        raise FileNotFoundError(f"Template not found: {template_path}")

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    if max_val >= confidence:
        return max_loc
    return None
