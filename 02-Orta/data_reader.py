import pandas as pd
from pathlib import Path


class DataReader:
    """Excel dosyasini okuyup regex filtresi uygulayan sinif."""

    def __init__(self, file_path: str = "../Data/Vadesiz_Hesap_Detay.xlsx") -> None:
        # resolve the file path relative to this file so that the bot can be
        # executed from any working directory
        self.file_path = Path(__file__).resolve().parent.joinpath(file_path).resolve()
        self.data: pd.DataFrame | None = None
        self.aciklama_col: str | None = None
        self.tutar_col: str | None = None
        # row index that contains the real headers in the Excel file
        self.header_row = 23
        self.pattern = r'^POSH.*\/\d{15}$'

    def read_excel(self) -> bool:
        try:
            if not self.file_path.exists():
                raise FileNotFoundError(f"Excel dosyasi bulunamadi: {self.file_path}")
            # the excel contains informational rows before the headers,
            # therefore pass the known header row index when reading
            self.data = pd.read_excel(self.file_path, header=self.header_row)
            print(f"\u2705 Excel okundu: {len(self.data)} satir")
            return True
        except Exception as exc:
            print(f"\u274C Okuma hatasi: {exc}")
            return False

    def filter_by_pattern(self) -> list[dict[str, str | float]]:
        if self.data is None:
            return []
        # print the column names for debugging purposes
        print(f"Mevcut sütunlar: {list(self.data.columns)}")

        # find the column that contains 'açıklama'
        aciklama_cols = [col for col in self.data.columns if 'açıklama' in str(col).lower()]
        if aciklama_cols:
            aciklama_col = aciklama_cols[0]
        else:
            # fallback to the third column if none match
            aciklama_col = self.data.columns[2]

        # store for external use
        self.aciklama_col = aciklama_col

        # find the column that contains 'tutar'
        tutar_cols = [col for col in self.data.columns if 'tutar' in str(col).lower()]
        if tutar_cols:
            tutar_col = tutar_cols[0]
        else:
            tutar_col = self.data.columns[3]

        self.tutar_col = tutar_col

        filtered = self.data[self.data[aciklama_col].astype(str).str.match(self.pattern, na=False)]
        print(f"🔍 Pattern eslesmesi: {len(filtered)} kayit")
        return filtered.to_dict("records")
