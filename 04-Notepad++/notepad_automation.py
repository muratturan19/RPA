"""Automates basic interactions with Notepad++ using PyAutoGUI, OCR and vision utilities."""
from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Optional, Tuple

import pyautogui

from ocr_utils import ocr_screen
from vision_utils import locate_on_screen


class NotepadPPAutomation:
    """Simple helper for automating Notepad++ actions."""

    def __init__(self, executable: str = "notepad++"):
        self.executable = executable

    def launch(self) -> None:
        """Launch Notepad++ application."""
        subprocess.Popen([self.executable])
        time.sleep(2)  # wait for the window to appear

    def new_file(self) -> None:
        """Open a new blank document in Notepad++."""
        pyautogui.hotkey("ctrl", "n")
        time.sleep(0.2)

    def write_text(self, text: str, interval: float = 0.05) -> None:
        """Type text into the active Notepad++ window."""
        pyautogui.typewrite(text, interval=interval)

    def save_file(self, path: str) -> None:
        """Save the current document to the given path."""
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.5)
        pyautogui.typewrite(path)
        pyautogui.press("enter")

    def close(self) -> None:
        """Close the active Notepad++ window."""
        pyautogui.hotkey("alt", "f4")
        time.sleep(0.5)

    # --- Mouse based interactions ---------------------------------
    def new_file_mouse(self, image_dir: str = "images") -> None:
        """Open a new file by clicking menu items instead of using hotkeys.

        Parameters
        ----------
        image_dir: str
            Directory containing the screenshot templates like
            ``file_menu.png`` and ``new_file.png`` used for visual search.
        """
        self.click_menu(Path(image_dir) / "file_menu.png")
        time.sleep(0.2)
        self.click_menu(Path(image_dir) / "new_file.png")
        time.sleep(0.2)

    def save_file_mouse(self, path: str, image_dir: str = "images") -> None:
        """Save the current document using mouse clicks.

        This method avoids keyboard shortcuts by opening the *File* menu and
        clicking the *Save* option through template matching.
        """
        self.click_menu(Path(image_dir) / "file_menu.png")
        time.sleep(0.2)
        self.click_menu(Path(image_dir) / "save_file.png")
        time.sleep(0.5)
        pyautogui.typewrite(path)
        pyautogui.press("enter")

    def close_mouse(self, image_dir: str = "images") -> None:
        """Close Notepad++ by clicking the window close button."""
        self.click_menu(Path(image_dir) / "close_button.png")
        time.sleep(0.5)

    def click_menu(self, image_path: str, confidence: float = 0.8) -> bool:
        """Click a menu or button identified by an image template."""
        location = locate_on_screen(image_path, confidence)
        if location:
            x, y = location
            pyautogui.click(x + 5, y + 5)
            return True
        return False

    def read_editor_text(self, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """Read text from the editor area using OCR."""
        return ocr_screen(region)
