"""RPA loglama modülü."""

from __future__ import annotations

import logging
import datetime
import pandas as pd
from pathlib import Path


class RPALogger:
    """RPA işlemleri için logger sınıfı."""

    def __init__(self) -> None:
        # Logs klasörünü oluştur
        Path("logs").mkdir(exist_ok=True)

        # Logger ayarları
        self.logger = logging.getLogger("RPA_Bot")
        self.logger.setLevel(logging.INFO)

        # Dosya handler
        file_handler = logging.FileHandler("logs/rpa_log.txt", encoding="utf-8")
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.results: list[dict[str, str]] = []

    def log_info(self, message: str) -> None:
        """Bilgi mesajı yaz."""
        self.logger.info(message)

    def log_error(self, message: str) -> None:
        """Hata mesajı yaz."""
        self.logger.error(message)

    def log_success(self, row_data: dict[str, str | float], status: str = "BAŞARILI") -> None:
        """İşlem sonucunu kaydet."""
        result = {
            "Zaman": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Tarih": row_data.get("Tarih", ""),
            "Açıklama": row_data.get("Açıklama", ""),
            "Tutar": row_data.get("Tutar", ""),
            "Durum": status,
        }
        self.results.append(result)
        self.log_info(
            f"İşlem kaydedildi: {row_data.get('Açıklama', '')} - {row_data.get('Tutar', '')} TL"
        )

    def save_results(self) -> None:
        """Sonuçları Excel'e kaydet."""
        if self.results:
            df = pd.DataFrame(self.results)
            Path("data").mkdir(exist_ok=True)
            df.to_excel("data/sonuclar.xlsx", index=False)
            self.log_info(f"Sonuçlar kaydedildi: {len(self.results)} işlem")
