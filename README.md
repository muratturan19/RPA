# 🤖 RPA Öğrenme Projesi

Python ile Excel'den GUI formuna otomatik veri transferi öğrenme platformu.

## 📊 Proje Özellikleri
- Gerçek banka işlem verisi kullanımı
- POSH pattern filtreleme (15 haneli sayı ile biten)
- Threading ile GUI donmaması
- Renkli log sistemi
- Modern Tkinter arayüzü

## 🌟 Veri Formatı
- **POS Satış işlemleri**: 25 adet
- **ÜİY Komisyon işlemleri**: 23 adet  
- **Toplam Net**: 84,058.40 TL
- **Pattern**: `^POSH.*\/\d{15}$`

## 🚀 Kullanım
1. `pip install -r requirements.txt`
2. `python create_real_data.py` (test verisi oluştur)
3. `python main.py` (ana program)
