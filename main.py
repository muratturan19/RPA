"""Uygulama başlangıç noktası."""

from __future__ import annotations

import time
import threading

# Global değişken
gui_app = None


def start_gui():
    """Sadece GUI'yi başlatır"""
    global gui_app
    from gui_app import BankGUI

    gui_app = BankGUI()
    gui_app.run()


def start_bot():
    """RPA bot'unu başlatır"""
    global gui_app

    if gui_app is None:
        print("\u274C GUI penceresi bulunamadı. Önce GUI'yi başlatın (seçenek 1 veya 3).")
        return

    try:
        from rpa_bot import RPABot

        bot = RPABot()
        bot.set_gui_reference(gui_app)  # GUI referansını ver
        bot.run()

    except Exception as e:
        print(f"\u274C RPA Bot hatası: {e}")


def start_both():
    """Hem GUI hem RPA'yı başlatır"""
    global gui_app

    print("\U0001F5A5\ufe0f GUI başlatılıyor...")

    # GUI'yi non-blocking başlat
    from gui_app import BankGUI
    gui_app = BankGUI()

    # GUI'yi ayrı thread'de çalıştır
    def run_gui():
        gui_app.mainloop()

    gui_thread = threading.Thread(target=run_gui, daemon=True)
    gui_thread.start()

    # GUI yüklensin diye kısa bekle
    time.sleep(2)

    print("\U0001F916 RPA Bot başlatılıyor...")
    start_bot()


def show_test_data():
    """Test verilerini gösterir"""
    try:
        from data_reader import DataReader

        reader = DataReader()
        if reader.read_excel():
            data = reader.get_data()
            print(f"\n\U0001F4CA Test Verisi ({len(data)} satır):")
            print("-" * 60)

            for i, row in enumerate(data[:10], 1):  # İlk 10 satır
                print(f"{i:2d}. {row['Tarih']} | {row['Tip']:12} | {row['Tutar']:>8} TL | {row['Açıklama']}")

            if len(data) > 10:
                print(f"... ve {len(data) - 10} satır daha")

            summary = reader.get_summary()
            if summary:
                print(f"\n\U0001F4CB Özet:")
                print(f"\U0001F4B3 POS Satış: {summary['pos_satis_adet']} adet, {summary['pos_satis_toplam']:.2f} TL")
                print(f"\U0001F4B8 ÜİY Komisyon: {summary['uiy_komisyon_adet']} adet, {summary['uiy_komisyon_toplam']:.2f} TL")
        else:
            print("\u274C Test verisi okunamadı. Önce 'python create_real_data.py' çalıştırın.")

    except Exception as e:
        print(f"\u274C Veri okuma hatası: {e}")


def main():
    """Ana menü"""
    while True:
        print("\n" + "=" * 50)
        print("\U0001F916 RPA Öğrenme Projesi")
        print("=" * 50)
        print("1) Sadece GUI'yi başlat")
        print("2) Sadece RPA botu çalıştır")
        print("3) Her ikisini başlat")
        print("4) Test verilerini göster")
        print("0) Çıkış")

        try:
            choice = input("\nSeçiminiz: ").strip()

            if choice == "1":
                start_gui()
            elif choice == "2":
                start_bot()
            elif choice == "3":
                start_both()
            elif choice == "4":
                show_test_data()
            elif choice == "0":
                print("\U0001F44B Görüşürüz!")
                break
            else:
                print("\u274C Geçersiz seçim! Lütfen 0-4 arası bir sayı girin.")

        except KeyboardInterrupt:
            print("\n\U0001F44B Programdan çıkılıyor...")
            break
        except Exception as e:
            print(f"\u274C Hata: {e}")


if __name__ == "__main__":
    main()
