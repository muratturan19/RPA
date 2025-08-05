"""Automates basic interactions with Notepad++ using PyAutoGUI, OCR and vision utilities."""
from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Dict, Optional, Tuple

import pyautogui
import pyperclip

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

    def _focus_editor(self) -> None:
        """Ensure the main editor window is focused.

        This helper activates the Notepad++ window, closes any stray
        dialogs such as the *Find* panel with ``ESC`` and finally clicks
        inside the editor area so that subsequent keyboard input is
        directed to the correct location.
        """
        windows = pyautogui.getWindowsWithTitle("Notepad++")
        if not windows:
            return
        win = windows[0]
        win.activate()
        # give the OS some time to bring the window to the foreground
        time.sleep(0.5)
        # close any pop-ups like the "Find" dialog
        pyautogui.press("esc")
        # click roughly in the centre of the window to focus the editor
        center_x = win.left + win.width // 2
        center_y = win.top + win.height // 2
        pyautogui.click(center_x, center_y)
        time.sleep(0.2)

    def launch(self) -> None:
        """Launch Notepad++ application and focus the editor."""
        subprocess.Popen([self.executable])
        # wait for the window to appear before attempting to focus
        time.sleep(2)
        self._focus_editor()

    def new_file(self) -> None:
        """Open a new blank document in Notepad++."""
        pyautogui.hotkey("ctrl", "n")
        time.sleep(0.2)

    def write_text(
        self, text: str, interval: float = 0.05, use_clipboard: bool = True
    ) -> None:
        """Type text into the active Notepad++ editor.

        Parameters
        ----------
        text: str
            The string to type.
        interval: float, optional
            Delay between each character when ``use_clipboard`` is ``False``.
        use_clipboard: bool, optional
            If ``True`` (default) the text is copied to the clipboard and
            pasted with ``Ctrl+V``. This avoids triggering unwanted keyboard
            shortcuts (e.g. ``Ctrl+Alt+I``) when characters require ``AltGr``.
            When set to ``False`` characters are sent one by one with the
            specified ``interval``.
        """
        self._focus_editor()
        if use_clipboard:
            pyperclip.copy(text)
            time.sleep(0.1)
            pyautogui.hotkey("ctrl", "v")
        else:
            for char in text:
                pyautogui.write(char)
                time.sleep(interval)

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
    def new_file_mouse(self, image_dir: str = "images", confidence: float = 0.9) -> None:
        """Open a new file by clicking menu items instead of using hotkeys.

        Parameters
        ----------
        image_dir: str
            Directory containing screenshot templates. By default the
            automation expects sequentially named files such as ``1.jpg``
            (File menu) and ``2.jpg`` (New file).
        confidence: float, optional
            Image match confidence forwarded to :meth:`click_menu`.
        """
        # Ensure editor window is active and close any pop-ups like the
        # advanced search panel before using image-based clicks.
        self._focus_editor()

        file_menu = Path(image_dir) / self.templates["file_menu"]
        new_file = Path(image_dir) / self.templates["new_file"]
        self.click_menu(file_menu, confidence)
        time.sleep(0.2)
        self.click_menu(new_file, confidence)
        time.sleep(0.2)

    def save_file_mouse(self, path: str, image_dir: str = "images", confidence: float = 0.9) -> None:
        """Save the current document using mouse clicks.

        This method avoids keyboard shortcuts by opening the *File* menu and
        clicking the *Save* option through template matching.

        Parameters
        ----------
        path: str
            File path to save to.
        image_dir: str
            Directory containing screenshot templates.
        confidence: float, optional
            Image match confidence forwarded to :meth:`click_menu`.
        """
        file_menu = Path(image_dir) / self.templates["file_menu"]
        save_file = Path(image_dir) / self.templates["save_file"]
        self.click_menu(file_menu, confidence)
        time.sleep(0.2)
        self.click_menu(save_file, confidence)
        time.sleep(0.5)
        pyautogui.typewrite(path)
        pyautogui.press("enter")

    def close_mouse(self, image_dir: str = "images", confidence: float = 0.9) -> None:
        """Close Notepad++ by clicking the window close button.

        Parameters
        ----------
        image_dir: str
            Directory containing screenshot templates.
        confidence: float, optional
            Image match confidence forwarded to :meth:`click_menu`.
        """
        close_button = Path(image_dir) / self.templates["close_button"]
        self.click_menu(close_button, confidence)
        time.sleep(0.5)

    def click_menu(self, image_path: str, confidence: float = 0.9) -> bool:
        """Click a menu or button identified by an image template.

        Parameters
        ----------
        image_path: str
            Path to the screenshot template to match.
        confidence: float, optional
            Matching threshold used by image recognition. Increasing the
            value can reduce false positives when screen colours or
            resolutions differ.
        """
        location = locate_on_screen(image_path, confidence)
        if location:
            x, y = location
            pyautogui.click(x + 5, y + 5)
            return True
        return False

    def read_editor_text(self, region: Optional[Tuple[int, int, int, int]] = None) -> str:
        """Read text from the editor area using OCR."""
        return ocr_screen(region)
