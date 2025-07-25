"""Excel veri okuma modülü."""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import re

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


class DataReader:
    """Excel dosyasını okur ve doğrular."""

    def __init__(self, file_path: str = "data/girdi_verisi.xlsx") -> None:
        self.file_path = file_path
        self.data: pd.DataFrame | None = None
        # Doğru pattern: POSH ile başlayan ve 15 haneli sayı ile biten
        self.valid_pattern = r'^POSH.*\/\d{15}$'

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

    def filter_posh_transactions(self, original_data: list[dict[str, str | float]] | None) -> list[dict[str, str | float]]:
        """Orijinal POSH işlemlerini filtreler."""
        if original_data is None:
            return []

        filtered_data: list[dict[str, str | float]] = []
        for item in original_data:
            aciklama = str(item.get('Açıklama', ''))
            if re.match(self.valid_pattern, aciklama):
                terminal_match = re.search(r'/([A-Z0-9]+)\s+[A-Z]\s+P\s+', aciklama)
                terminal = terminal_match.group(1) if terminal_match else ''

                if 'POS Satış' in aciklama:
                    tip = 'POS Satış'
                    kisa_aciklama = f"POS Satış - Terminal {terminal}" if terminal else 'POS Satış'
                elif 'ÜİY Komisyon' in aciklama:
                    tip = 'ÜİY Komisyon'
                    kisa_aciklama = 'ÜİY Komisyon Kesinti'
                else:
                    tip = 'Diğer'
                    kisa_aciklama = aciklama[:50] + '...' if len(aciklama) > 50 else aciklama

                filtered_data.append({
                    'Tarih': item.get('Tarih', ''),
                    'Açıklama': kisa_aciklama,
                    'Tutar': item.get('Tutar', 0),
                    'Tip': tip,
                    'Terminal': terminal,
                    'Orijinal_Açıklama': aciklama,
                })

        print(f"🔍 Pattern kontrolü: {len(filtered_data)} geçerli işlem bulundu")
        return filtered_data

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

    def get_summary(self) -> dict[str, int | float] | None:
        """Veri özeti döndürür."""
        if self.data is not None:
            pos_satis = self.data[self.data['Tip'] == 'POS Satış']
            uiy_komisyon = self.data[self.data['Tip'] == 'ÜİY Komisyon']

            return {
                'toplam_islem': len(self.data),
                'pos_satis_adet': len(pos_satis),
                'uiy_komisyon_adet': len(uiy_komisyon),
                'pos_satis_toplam': pos_satis['Tutar'].sum() if len(pos_satis) > 0 else 0,
                'uiy_komisyon_toplam': uiy_komisyon['Tutar'].sum() if len(uiy_komisyon) > 0 else 0,
            }
        return None
