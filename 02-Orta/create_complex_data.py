import pandas as pd
from pathlib import Path


def create_data(file_path: str = "../data/complex_data.xlsx") -> None:
    """Karma\u015f\u0131k test verisi olu\u015fturur."""
    data = [
        {"Tarih": "01.08.2025", "Açıklama": "POSH GARANTİ MAGAZA/123456789012345", "Tutar": 1500.25},
        {"Tarih": "01.08.2025", "Açıklama": "POSH XYZ/123456789012345", "Tutar": 500.0},
        {"Tarih": "01.08.2025", "Açıklama": "POS SATIŞ YANLIŞ/12345", "Tutar": 100.0},
        {"Tarih": "01.08.2025", "Açıklama": "POSH DENEME/000000000000000", "Tutar": 2000.0},
        {"Tarih": "01.08.2025", "Açıklama": "DİĞER İŞLEM", "Tutar": 50.0},
    ]
    df = pd.DataFrame(data)
    Path("../data").mkdir(exist_ok=True)
    df.to_excel(file_path, index=False)
    print(f"\u2705 Test verisi olusturuldu: {file_path} ({len(df)} kayit)")


if __name__ == "__main__":
    create_data()
