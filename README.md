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

# 🚀 Kurulum ve Çalıştırma

## 🔧 Otomatik Kurulum (Önerilen)
```bash
# 1. Repo'yu klonla
git clone https://github.com/kullanici/RPA.git
cd RPA

# 2. Ortam kontrolü ve otomatik kurulum
python check_environment.py

# 3. Test verilerini oluştur
python create_real_data.py

# 4. Çalıştır
python main.py
```

### 🛠️ Manuel Kurulum
```bash
pip install pandas>=2.0.0 openpyxl>=3.1.0 colorama>=0.4.0
```

✅ Desteklenen Platformlar

- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)
- Python 3.8+

## 🎯 Bu Şekilde:
1. ✅ Her bilgisayarda otomatik kontrol
2. ✅ Eksik paketleri otomatik kurar
3. ✅ Hata durumunda net açıklama  
4. ✅ Platform bağımsız çalışır
