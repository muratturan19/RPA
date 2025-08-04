# 04 - Notepad++ RPA Sistemi

Bu klasör, `03-Karmasik` modülünün kopyası üzerine Notepad++ otomasyonunu ekler. PyAutoGUI tabanlı etkileşim, `pytesseract` ile OCR ve OpenCV ile görsel eşleştirme sağlayan ek modüller içerir.

## Gereksinimler

Gerekli paketleri aşağıdaki komut ile kurabilirsiniz:

```bash
pip install -r requirements.txt
```

## Çalıştırma

Komut satırından `main.py` dosyasını çalıştırarak menülü sistemi başlatabilirsiniz. Program açıldığında aşağıdaki seçenekleri içeren bir menü gelir:

1. Sadece gelişmiş GUI'yi başlatır.
2. GUI açıkken yalnızca RPA botunu çalıştırır.
3. GUI ile RPA botunu entegre şekilde (demo modunda) başlatır.
4. Streamlit web arayüzünü açar.
5. Sistem bilgilerini gösterir.
6. Demo senaryolarını listeler.
7. Notepad++ otomasyon demosunu çalıştırır.

Örneğin menülü mod ile başlamak için:
```bash
python main.py
```

Sadece Streamlit panelini başlatmak isterseniz:
```bash
streamlit run app.py
```

Streamlit paneli üzerinden Excel dosyalarını yükleyip işle başlatabilirsiniz. Panel, `app.py` dosyasında tanımlıdır ve arka planda `main.py` üzerinden RPA botunu tetikler.

## Dosya Yapısı

- `advanced_gui.py`: Gelişmiş Tkinter tabanlı ERP arayüzü
- `rpa_bot.py`: Excel verilerini bu arayüz üzerinden işleyen otomasyon botu
- `app.py`: Drag & Drop özellikli Streamlit paneli
- `main.py`: Yukarıdaki bileşenleri yöneten ana kontrol merkezi

## Adım Onayı

RPA botu her adımın ardından kullanıcıya "Devam edilsin mi?" sorusunu içeren
bir onay penceresi gösterir. "HAYIR" seçilirse ilgili adım ve kalan süreç
iptal edilir. Bu sayede uzun işlemleri adım adım kontrol edebilirsiniz.

3. adımda bot ilk Excel dosyasını hızlıca okuyarak önizleme kaydı sayısını
hesaplar ve bu sayı GUI'de gösterilir. Eğer hiç kayıt bulunmazsa devam edip
etmeyeceğiniz sorulur.
