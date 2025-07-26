"""Gelişmiş RPA Sistemi - Ana Program"""

from __future__ import annotations
import threading
import time

# Global GUI referansı
gui_app = None

def start_gui() -> None:
    """Sadece GUI'yi başlat"""
    global gui_app
    from accounting_gui import AdvancedAccountingGUI

    gui_app = AdvancedAccountingGUI()
    gui_app.run()

def start_bot() -> None:
    """RPA bot'unu çalıştır (GUI açık olmalı)"""
    global gui_app

    if gui_app is None:
        print("❌ Önce GUI'yi açın (Seçenek 1 veya 3)")
        return

    from rpa_bot import AdvancedRPABot
    
    bot = AdvancedRPABot()
    bot.set_gui_reference(gui_app)
    bot.run()

def start_bot_threaded() -> threading.Thread | None:
    """RPA'yi thread'de çalıştır"""
    global gui_app

    if gui_app is None:
        print("❌ GUI referansı bulunamadı")
        return None

    from rpa_bot import AdvancedRPABot
    
    bot = AdvancedRPABot()
    bot.set_gui_reference(gui_app)
    return bot.run()

def start_both() -> None:
    """GUI + RPA birlikte başlat"""
    global gui_app

    print("🖥️ GUI başlatılıyor...")
    from accounting_gui import AdvancedAccountingGUI

    gui_app = AdvancedAccountingGUI()

    # GUI'yi öne getir
    gui_app.root.lift()
    gui_app.root.attributes('-topmost', True)
    gui_app.root.after(100, lambda: gui_app.root.attributes('-topmost', False))
    gui_app.root.focus_force()

    # RPA'yi 3 saniye sonra başlat (GUI tamamen yüklensin)
    gui_app.root.after(3000, start_bot_threaded)
    
    gui_app.run()

def show_demo_info():
    """Demo bilgilerini göster"""
    print("\n" + "="*60)
    print("🤖 GELİŞMİŞ RPA SİSTEMİ - DEMO BİLGİLERİ")
    print("="*60)
    print("📋 RPA ADIMLARI:")
    print("  1. Dashboard ekranında başlar")
    print("  2. 'Finans-Tahsilat' sekmesine tıklar")
    print("  3. 'Veri Giriş' butonuna tıklar")
    print("  4. Excel'den 77 kayıt okur")
    print("  5. Her kayıt için:")
    print("     - Tarih alanına tıklar → veri girer")
    print("     - Açıklama alanına tıklar → veri girer")
    print("     - Tutar alanına tıklar → veri girer")
    print("     - Kaydet butonuna tıklar")
    print("     - Form temizlenir")
    print("     - Sonraki kayda geçer")
    print("\n💡 ÖZELLIKLER:")
    print("  ✅ Gerçekçi GUI navigasyonu")
    print("  ✅ Modal pencere işlemleri") 
    print("  ✅ Adım adım loglama")
    print("  ✅ Threading ile GUI donmaması")
    print("  ✅ Ana tabloya kayıt ekleme")
    print("  ✅ Dashboard istatistik güncelleme")
    print("="*60)

def main() -> None:
    """Ana menü"""
    while True:
        print("\n" + "="*50)
        print("🤖 GELİŞMİŞ RPA SİSTEMİ")
        print("="*50)
        print("1) 🖥️  Sadece GUI'yi başlat")
        print("2) 🤖 RPA bot'unu çalıştır (GUI açık olmalı)")
        print("3) 🚀 Her ikisini birlikte başlat")
        print("4) 📋 Demo bilgilerini göster")
        print("0) ❌ Çıkış")
        print("="*50)
        
        try:
            choice = input("Seçiminiz (0-4): ").strip()
            
            if choice == "1":
                print("🖥️ GUI başlatılıyor...")
                start_gui()
                
            elif choice == "2":
                print("🤖 RPA bot çalıştırılıyor...")
                start_bot()
                
            elif choice == "3":
                print("🚀 GUI + RPA birlikte başlatılıyor...")
                start_both()
                
            elif choice == "4":
                show_demo_info()
                
            elif choice == "0":
                print("👋 Çıkış yapılıyor... İyi günler!")
                break
                
            else:
                print("❌ Geçersiz seçim! Lütfen 0-4 arası bir sayı girin.")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Kullanıcı tarafından iptal edildi")
            break
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    main()
