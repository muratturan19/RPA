# 01 - Basit RPA Örneği

Bu klasörde Excel verilerini basit bir Tkinter arayüzüne otomatik olarak girmek için hazırlanmış örnek bir RPA sistemi bulunmaktadır.

## Gereksinimler

Öncelikle bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

## Çalıştırma

1. Ortamın hazır olup olmadığını kontrol etmek için:
   ```bash
   python check_environment.py
   ```
2. Örnek veri oluşturmak için:
   ```bash
   python create_real_data.py
   ```
3. Ardından ana programı çalıştırın:
   ```bash
   python main.py
   ```

Program çalıştıktan sonra menüden GUI'yi açabilir ve `data_reader.py` tarafından okunan Excel kayıtlarının otomatik olarak girişinin yapılmasını izleyebilirsiniz.
