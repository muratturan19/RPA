from __future__ import annotations

import time
from pathlib import Path
from typing import Callable, Iterable
import pandas as pd

class EnterpriseRPABot:
    """Çoklu Excel dosyası işleyen basit RPA botu"""

    def __init__(self, gui=None) -> None:
        self.gui = gui
        self.results: list[dict[str, int | str]] = []

    def set_gui_reference(self, gui) -> None:
        self.gui = gui

    def _update_gui(self, message: str) -> None:
        if self.gui and hasattr(self.gui, "update_status"):
            self.gui.update_status(message)

    def process_record(self, record: dict) -> None:
        self._update_gui(f"Kayıt işleniyor: {record}")
        time.sleep(0.1)  # Simülasyon

    def process_excel(self, excel_path: Path) -> None:
        try:
            df = pd.read_excel(excel_path)
            records = df.to_dict("records")
        except Exception as exc:
            self.results.append(
                {"file": excel_path.name, "records": 0, "success": 0, "error": str(exc)}
            )
            return

        total = len(records)
        success = 0
        for rec in records:
            try:
                self.process_record(rec)
                success += 1
            except Exception:
                pass
        self.results.append(
            {"file": excel_path.name, "records": total, "success": success, "error": total - success}
        )

    def run(
        self,
        excel_files: Iterable[Path],
        progress_callback: Callable[[float, str], None] | None = None,
    ) -> None:
        files = list(excel_files)
        total = len(files)
        for i, path in enumerate(files, 1):
            if progress_callback:
                progress_callback((i - 1) / total, f"Başlıyor: {path.name}")
            self.process_excel(path)
            if progress_callback:
                progress_callback(i / total, f"Tamamlandı: {path.name}")
        if progress_callback:
            progress_callback(1.0, "Tüm dosyalar tamamlandı")

    def get_results(self) -> list[dict[str, int | str]]:
        return self.results
