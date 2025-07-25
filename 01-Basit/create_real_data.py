import pandas as pd
import re
from pathlib import Path

# Gerçek müşteri verisi - İlk 10 işlem (Eğitim için)
real_data = [
    {"Tarih": "23.07.2025", "Açıklama": "POS Satış - Terminal N042", "Tutar": 670.99, "Tip": "POS Satış"},
    {"Tarih": "23.07.2025", "Açıklama": "ÜİY Komisyon Kesinti", "Tutar": -13.42, "Tip": "ÜİY Komisyon"},
    {"Tarih": "23.07.2025", "Açıklama": "POS Satış - Terminal TY01", "Tutar": 307.49, "Tip": "POS Satış"},
    {"Tarih": "23.07.2025", "Açıklama": "ÜİY Komisyon Kesinti", "Tutar": -8.46, "Tip": "ÜİY Komisyon"},
    {"Tarih": "23.07.2025", "Açıklama": "POS Satış - Terminal N001", "Tutar": 4559.47, "Tip": "POS Satış"},
    {"Tarih": "23.07.2025", "Açıklama": "ÜİY Komisyon Kesinti", "Tutar": -125.39, "Tip": "ÜİY Komisyon"},
    {"Tarih": "23.07.2025", "Açıklama": "POS Satış - Terminal O002", "Tutar": 192.02, "Tip": "POS Satış"},
    {"Tarih": "23.07.2025", "Açıklama": "ÜİY Komisyon Kesinti", "Tutar": -5.28, "Tip": "ÜİY Komisyon"},
    {"Tarih": "23.07.2025", "Açıklama": "POS Satış - Terminal TY02", "Tutar": 1064.18, "Tip": "POS Satış"},
    {"Tarih": "23.07.2025", "Açıklama": "ÜİY Komisyon Kesinti", "Tutar": -29.26, "Tip": "ÜİY Komisyon"}
]

# DataFrame oluşur
df = pd.DataFrame(real_data)

# data klasörünü oluştur
Path("../data").mkdir(exist_ok=True)

# Excel dosyasını kaydet
df.to_excel("../data/girdi_verisi.xlsx", index=False)

print("✅ Gerçek müşteri verisi Excel'e kaydedildi: ../data/girdi_verisi.xlsx")
print(f"📊 {len(df)} satır gerçek işlem hazırlandı")
print("\n📋 Veri özeti:")
print(f"💳 POS Satış: {len(df[df['Tip'] == 'POS Satış'])} adet")
print(f"💸 ÜİY Komisyon: {len(df[df['Tip'] == 'ÜİY Komisyon'])} adet")
print(f"💰 POS Satış Toplamı: {df[df['Tip'] == 'POS Satış']['Tutar'].sum():.2f} TL")
print(f"💸 ÜİY Komisyon Toplamı: {df[df['Tip'] == 'ÜİY Komisyon']['Tutar'].sum():.2f} TL")

# Önizleme
print("\n🔍 Veri önizleme:")
print(df)
