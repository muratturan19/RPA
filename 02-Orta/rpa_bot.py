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
        for rec in records:
            desc = str(rec.get("Açıklama", ""))
            amount = float(rec.get("Tutar", 0))
            kategori = "Büyük İşlem" if amount > 1000 else "Normal"
            banka = "Garanti" if "GARANTİ" in desc.upper() else "Diğer"
            print(f"✅ {desc} | {amount:.2f} TL | {kategori} | Banka: {banka}")
