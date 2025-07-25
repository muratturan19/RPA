import pandas as pd
from pathlib import Path


class DataReader:
    """Excel dosyasini okuyup regex filtresi uygulayan sinif."""

    def __init__(self, file_path: str = "../Data/Vadesiz_Hesap_Detay.xlsx") -> None:
        self.file_path = file_path
        self.data: pd.DataFrame | None = None
        self.pattern = r'^POSH.*\/\d{15}$'

    def read_excel(self) -> bool:
        try:
            if not Path(self.file_path).exists():
                raise FileNotFoundError(f"Excel dosyasi bulunamadi: {self.file_path}")
            self.data = pd.read_excel(self.file_path)
            print(f"\u2705 Excel okundu: {len(self.data)} satir")
            return True
        except Exception as exc:
            print(f"\u274C Okuma hatasi: {exc}")
            return False

    def filter_by_pattern(self) -> list[dict[str, str | float]]:
        if self.data is None:
            return []
        filtered = self.data[self.data['Açıklama'].astype(str).str.match(self.pattern, na=False)]
        print(f"🔍 Pattern eslesmesi: {len(filtered)} kayit")
        return filtered.to_dict("records")
