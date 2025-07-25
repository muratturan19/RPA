"""RPA bot ana sınıfı."""

from __future__ import annotations

import time
import threading
import tkinter as tk
from tkinter import messagebox

try:
    import pyautogui
except Exception:  # pragma: no cover - pyautogui olmayabilir
    pyautogui = None

from data_reader import DataReader
from logger import RPALogger


class RPABot:
    """Excel verilerini GUI'ye otomatik giren bot."""

    def __init__(self, gui_title: str = "Banka İşlemleri Giriş Sistemi") -> None:
        self.gui_title = gui_title
        self.reader = DataReader()
        self.logger = RPALogger()
        self.is_running = False
        self.current_progress = 0

    def _find_gui(self) -> bool:
        """GUI penceresini bulur"""
        try:
            # GUI referansı varsa direkt kullan
            if hasattr(self, "gui_window") and self.gui_window:
                return True

            self.logger.log_error(
                "GUI referansı bulunamadı. set_gui_reference() çağrılmalı."
            )
            return False

        except Exception as e:
            self.logger.log_error(f"GUI arama hatası: {e}")
            return False

    def set_gui_reference(self, gui_window):
        """GUI referansını direkt olarak ayarlar"""
        self.gui_window = gui_window
        if hasattr(gui_window, "title"):
            self.gui_title = gui_window.title()
        else:
            self.gui_title = "GUI Penceresi"
        self.logger.log_info(f"GUI referansı ayarlandı: {self.gui_title}")
        return True

    def run(self) -> None:
        """Botu çalıştır."""
        if not self.reader.read_excel() or not self.reader.validate_data():
            self.logger.log_error("Veri okunamadı veya doğrulanamadı")
            return

        data_list = self.reader.get_data()
        if not self._find_gui():
            return
        if pyautogui is None:
            self.logger.log_error("pyautogui bulunamadı")
            return

        for idx, row in enumerate(data_list, start=1):
            self.logger.log_info(f"{idx}. satır işleniyor")
            try:
                pyautogui.write(row.get("Tarih", ""))
                pyautogui.press("tab")
                pyautogui.write(row.get("Açıklama", ""))
                pyautogui.press("tab")
                pyautogui.write(str(row.get("Tutar", "")))
                pyautogui.press("tab")
                pyautogui.write("6232011")
                pyautogui.press("tab")
                time.sleep(2)
                pyautogui.press("enter")  # Kaydet butonu
                time.sleep(1)
                self.logger.log_success(row)
            except Exception as exc:  # pragma: no cover - otomasyon hataları
                self.logger.log_error(str(exc))
        self.logger.save_results()

    def run_automation_threaded(self, gui_callback=None):
        """RPA'yı ayrı thread'de çalıştırır (GUI donmaması için)."""

        def automation_worker():
            self.is_running = True
            self.run()
            if gui_callback:
                gui_callback("completed")
            self.is_running = False

        thread = threading.Thread(target=automation_worker, daemon=True)
        thread.start()
        return thread
