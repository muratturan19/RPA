# 🤖 RPA Örnekleri

Bu repoda, Robotic Process Automation konseptini kademeli olarak öğreten dört ayrı proje yer alır. Her klasör bir öncekini temel alarak daha gelişmiş örnekler içerir.

## Klasörler

- **01-Basit/** – Excel verilerini Tkinter tabanlı basit bir forma otomatik girmek için hazırlanmış ilk öğrenme projesi.
- **02-Orta/** – "Muhasebe Pro" tarzı çok sekmeli ve araç çubuklu gelişmiş GUI. Excel yükledikten sonra kayıtları regex, tutar veya tarih filtreleriyle inceleme imkânı sunar.
- **03-Karmasik/** – Çoklu Excel dosyası işleyebilen, detaylı Tkinter arayüzüne ve Streamlit tabanlı web paneline sahip enterprise seviye bir sistem.
- **04-Notepad++/** – PyAutoGUI, OCR ve görsel eşleştirme kullanarak Notepad++ üzerinde metin oluşturma ve kaydetme otomasyonu yapar.
- **Data/** – Örnek Excel dosyalarını koyabileceğiniz klasör. Betikler `../Data` yolunu kullanır.

## Hızlı Başlangıç

### 01-Basit
```bash
cd 01-Basit
python check_environment.py
python create_real_data.py
python main.py
```

### 02-Orta
```bash
cd 02-Orta
python main.py
```

İsterseniz `accounting_gui.py` dosyasını tek başına çalıştırarak sadece arayüzü test edebilirsiniz.

### 03-Karmasik
```bash
cd 03-Karmasik
python main.py            # Terminal menülü mod
# veya
streamlit run app.py      # Web paneli
```

Kompleks sistemde GUI + RPA bütünleşik şekilde demo modunda çalıştırılabilir ve Streamlit paneli üzerinden sürükle‑bırak yöntemiyle Excel dosyaları yüklenebilir.

### 04-Notepad++
```bash
cd 04-Notepad++
python main.py
```
Menüden `7` seçeneğini kullanarak Notepad++ otomasyon demosunu çalıştırabilirsiniz.

## Gereksinimler

- `01-Basit/requirements.txt` temel paketleri içerir (pandas, openpyxl, pyautogui ...).
- `03-Karmasik/requirements.txt` ek olarak `streamlit` ve `reportlab` gibi kütüphaneler gerektirir.
- `04-Notepad++/requirements.txt` PyAutoGUI, Tesseract OCR ve OpenCV gibi ek bağımlılıklar içerir.

## Lisans

Bu projeler [MIT Lisansı](LICENSE) ile yayınlanmaktadır.
