"""Automates basic interactions with Notepad++ using PyAutoGUI, OCR and vision utilities."""
from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import pyautogui

from ocr_utils import ocr_screen
from vision_utils import locate_on_screen


# Windows sistemlerde Notepad++ uygulamasının varsayılan kurulum yolu.
NOTEPAD_PATH = r"D:\\Program Files\\Notepad++\\notepad++.exe"


class NotepadPPAutomation:
    """Simple helper for automating Notepad++ actions."""

    # Default mapping for numbered screenshot templates
    DEFAULT_TEMPLATES: Dict[str, str] = {
        "file_menu": "1.jpg",
        "new_file": "2.jpg",
        "save_file": "3.jpg",
        "close_button": "4.jpg",
    }

    def __init__(
        self,
        executable: str = NOTEPAD_PATH,
        templates: Optional[Dict[str, str]] = None,
    ) -> None:
        self.executable = executable
        # Allow overriding of template filenames
        self.templates = {**self.DEFAULT_TEMPLATES, **(templates or {})}

    def launch(self) -> None:
        """Launch Notepad++ application."""
        subprocess.Popen([self.executable])
        time.sleep(2)  # wait for the window to appear
        # Bring the application window to the foreground so that
        # subsequent keyboard commands target Notepad++.
        windows = pyautogui.getWindowsWithTitle("Notepad++")
        if windows:
            windows[0].activate()
            time.sleep(0.2)

    def new_file(self) -> None:
        """Open a new blank document in Notepad++."""
        pyautogui.hotkey("ctrl", "n")
        time.sleep(0.2)

    def write_text(self, text: str, interval: float = 0.05) -> None:
        """Type text into the active Notepad++ window."""
        pyautogui.typewrite(text, interval=interval)

    def save_file(self, path: str) -> None:
        """Save the current document to the given path.

        ``Ctrl+Shift+S`` is used to always trigger the *Save As* dialog
        even if the document already has a filename. This prevents
        accidental typing into the editor when no dialog appears.
        """
        pyautogui.hotkey("ctrl", "shift", "s")
        time.sleep(0.5)
        pyautogui.typewrite(path)
        pyautogui.press("enter")
        time.sleep(0.5)

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
            Directory containing screenshot templates. By default the
            automation expects sequentially named files such as ``1.jpg``
            (File menu) and ``2.jpg`` (New file).
        """
        file_menu = Path(image_dir) / self.templates["file_menu"]
        new_file = Path(image_dir) / self.templates["new_file"]
        self.click_menu(file_menu)
        time.sleep(0.2)
        self.click_menu(new_file)
        time.sleep(0.2)

    def save_file_mouse(self, path: str, image_dir: str = "images") -> None:
        """Save the current document using mouse clicks.

        This method avoids keyboard shortcuts by opening the *File* menu and
        clicking the *Save* option through template matching.
        """
        file_menu = Path(image_dir) / self.templates["file_menu"]
        save_file = Path(image_dir) / self.templates["save_file"]
        self.click_menu(file_menu)
        time.sleep(0.2)
        self.click_menu(save_file)
        time.sleep(0.5)
        pyautogui.typewrite(path)
        pyautogui.press("enter")

    def close_mouse(self, image_dir: str = "images") -> None:
        """Close Notepad++ by clicking the window close button."""
        close_button = Path(image_dir) / self.templates["close_button"]
        self.click_menu(close_button)
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
