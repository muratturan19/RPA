from __future__ import annotations

from data_reader import DataReader


class RPABot:
    """Conditional logic bot."""

    def __init__(self) -> None:
        self.reader = DataReader()

    def run(self) -> None:
        """Verileri oku ve kosullu isle."""
        if not self.reader.read_excel():
            return
        records = self.reader.filter_by_pattern()
        desc_col = self.reader.aciklama_col or "Açıklama"
        tutar_col = self.reader.tutar_col or "Tutar"

        for rec in records:
            desc = str(rec.get(desc_col, ""))
            amount = float(rec.get(tutar_col, 0))
            kategori = "Büyük İşlem" if amount > 1000 else "Normal"
            banka = "Garanti" if "GARANTİ" in desc.upper() else "Diğer"
            print(f"✅ {desc} | {amount:.2f} TL | {kategori} | Banka: {banka}")
