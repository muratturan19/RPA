"""RPA bot ana sınıfı."""

from __future__ import annotations

import time
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

    def _find_gui(self) -> bool:
        """GUI açık mı kontrol et."""
        for w in tk._default_root.winfo_children() if tk._default_root else []:
            if w.title() == self.gui_title:
                return True
        messagebox.showerror("Hata", "GUI uygulaması bulunamadı")
        return False

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
