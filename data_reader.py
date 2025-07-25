"""Excel veri okuma modülü."""

from __future__ import annotations

from pathlib import Path
import pandas as pd

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


class DataReader:
    """Excel dosyasını okur ve doğrular."""

    def __init__(self, file_path: str = "data/girdi_verisi.xlsx") -> None:
        self.file_path = file_path
        self.data: pd.DataFrame | None = None

    def read_excel(self) -> bool:
        """Excel dosyasını oku."""
        try:
            if not Path(self.file_path).exists():
                raise FileNotFoundError(f"Excel dosyası bulunamadı: {self.file_path}")

            self.data = pd.read_excel(self.file_path)
            print(f"{GREEN}\u2705 Excel dosyası okundu: {len(self.data)} satır{RESET}")
            return True
        except Exception as e:  # pragma: no cover - basit çıktı
            print(f"{RED}\u274C Excel okuma hatası: {e}{RESET}")
            return False

    def get_data(self) -> list[dict[str, str | float]]:
        """Okunan veriyi döndür."""
        if self.data is not None:
            return self.data.to_dict("records")
        return []

    def validate_data(self) -> bool:
        """Gerekli sütunları kontrol et."""
        required_columns = ["Tarih", "Açıklama", "Tutar", "Tip"]
        if self.data is not None:
            missing_cols = [col for col in required_columns if col not in self.data.columns]
            if missing_cols:
                print(f"{RED}\u274C Eksik sütunlar: {missing_cols}{RESET}")
                return False
            return True
        return False
