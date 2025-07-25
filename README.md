# 🤖 RPA Örnekleri

Bu repo, basitten karmaşığa doğru ilerleyen çeşitli RPA (Robotic Process Automation) örneklerini içerir.

## Klasörler

- **01-Basit/**: Orijinal öğrenme projesi. Excel verilerini Tkinter tabanlı arayüze otomatik girer.
- **02-Orta/**: Presto benzeri gelişmiş GUI. Seçilen Excel dosyasındaki verileri regex ile filtreler. Varsayılan filtre `^POSH.*MUSLUOĞLU$` şeklindedir.
- **03-Karmasik/**: Daha ileri senaryolar için boş bırakılmış klasör.
- **data/**: Excel dosyalarınızı koyabileceğiniz klasör. `01-Basit` ve `02-Orta` betikleri bu klasörün bir üstündeki `../data` yolunu kullanır.

## Basit Proje Nasıl Çalıştırılır?

```bash
cd 01-Basit
python check_environment.py
python create_real_data.py
python main.py
```

`02-Orta/presto_gui.py` dosyasını doğrudan çalıştırarak karmaşık arayüzü deneyebilirsiniz.
