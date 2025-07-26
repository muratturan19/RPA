# 03 - Karmaşık RPA Sistemi

Bu klasör, çoklu Excel dosyası işleyebilen, gelişmiş Tkinter arayüzüne ve Streamlit tabanlı web paneline sahip örnek bir karmaşık RPA uygulamasını içerir.

## Gereksinimler

Gerekli paketleri aşağıdaki komut ile kurabilirsiniz:

```bash
pip install -r requirements.txt
```

## Çalıştırma

Komut satırından `main.py` dosyasını çalıştırarak sistemi başlatabilirsiniz. Program açıldığında aşağıdaki seçenekleri içeren bir menü gelir:

1. Sadece gelişmiş GUI'yi başlatır.
2. GUI açıkken yalnızca RPA botunu çalıştırır.
3. GUI ile RPA botunu entegre şekilde (demo modunda) başlatır.
4. Streamlit web arayüzünü açar.

Örneğin menülü mod ile başlamak için:
```bash
python main.py
```

Sadece Streamlit panelini başlatmak isterseniz:
```bash
python main.py --mode streamlit
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
