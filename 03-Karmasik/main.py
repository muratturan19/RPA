"""
Karmaşık RPA Sistemi - Ana Koordinasyon Merkezi
Streamlit entegrasyonu + Terminal menü + Multi-threading yönetimi
"""
from __future__ import annotations

import sys
import argparse
import threading
import time
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional
import subprocess
import json
import signal
import atexit

# Global referanslar
gui_app = None
rpa_bot = None
active_threads = []
streamlit_process = None


def parse_command_line_args():
    """Komut satırı argümanlarını parse et"""
    parser = argparse.ArgumentParser(description='Karmaşık RPA Sistemi')
    parser.add_argument('--files', nargs='*', help='İşlenecek Excel dosya yolları')
    parser.add_argument('--mode', choices=['gui', 'rpa', 'both', 'streamlit'], 
                       default='terminal', help='Çalışma modu')
    parser.add_argument('--speed', choices=['slow', 'normal', 'fast'], 
                       default='normal', help='RPA işlem hızı')
    parser.add_argument('--headless', action='store_true', 
                       help='GUI göstermeden çalıştır')
    parser.add_argument('--port', type=int, default=8501, 
                       help='Streamlit port numarası')

    return parser.parse_args()


def print_banner():
    """Sistem banner'ını yazdır"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    🤖 KARMAŞIK RPA SİSTEMİ                   ║
║                   Enterprise Seviye v3.0                    ║
╠══════════════════════════════════════════════════════════════╣
║  🎯 Özellikler:                                              ║
║  • Streamlit Web Arayüzü (Drag & Drop)                     ║
║  • 6 Adımlı Karmaşık GUI Navigasyonu                       ║
║  • Çoklu Excel Dosya İşleme                                ║
║  • Enterprise Seviye Raporlama                             ║
║  • Gerçek Mouse Hareketleri                                ║
║  • Multi-threading Desteği                                 ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def start_gui_only() -> None:
    """Sadece Enterprise GUI'yi başlat"""
    global gui_app

    print("🖥️ Enterprise GUI başlatılıyor...")
    print("📊 Karmaşık navigasyon sistemi yükleniyor...")

    from gui.base_gui import EnterpriseGUI

    gui_app = EnterpriseGUI()
    print("✅ GUI hazır - Enterprise ERP Sistemi aktif")
    gui_app.run()


def start_rpa_only() -> None:
    """Sadece RPA bot'unu çalıştır (GUI açık olmalı)"""
    global gui_app, rpa_bot

    if gui_app is None:
        print("❌ RPA çalıştırmak için önce GUI'yi açın (Seçenek 1 veya 3)")
        return

    print("🤖 RPA bot'u başlatılıyor...")

    from rpa.core_engine import EnterpriseRPABot

    rpa_bot = EnterpriseRPABot()
    rpa_bot.set_gui_reference(gui_app)

    # Varsayılan dosyaları yükle
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir = Path("../data")

    excel_files = list(data_dir.glob("*.xlsx")) if data_dir.exists() else []

    if excel_files:
        print(f"📁 {len(excel_files)} Excel dosyası bulundu")
        rpa_bot.run(excel_files)
    else:
        print("⚠️ Excel dosyası bulunamadı, test modu çalışacak")
        rpa_bot.run([])


def start_both_integrated() -> None:
    """GUI + RPA entegre başlatma - Sunum modu"""
    global gui_app, rpa_bot

    print("🚀 ENTEGRE SISTEM BAŞLATILUYOR...")
    print("🎬 Sunum modu aktif - Canlı demo")
    print("📊 Dashboard + RPA eş zamanlı çalışacak")
    print("🎨 Enterprise tema aktif")

    from gui.base_gui import EnterpriseGUI
    from rpa.core_engine import EnterpriseRPABot

    # GUI'yi başlat
    gui_app = EnterpriseGUI()

    # RPA'yi hazırla
    rpa_bot = EnterpriseRPABot()
    rpa_bot.set_gui_reference(gui_app)
    rpa_bot.set_processing_speed("normal")  # Demo için normal hız

    # Varsayılan dosyaları hazırla
    data_dir = Path("data")
    if not data_dir.exists():
        data_dir = Path("../data")

    excel_files = list(data_dir.glob("*.xlsx")) if data_dir.exists() else []

    if excel_files:
        gui_app.set_processing_files(excel_files)

    # GUI'yi tam ekran yap ve öne getir
    gui_app.root.state('zoomed')
    gui_app.root.attributes('-topmost', True)
    gui_app.root.after(200, lambda: gui_app.root.attributes('-topmost', False))

    # RPA'yi 2 saniye sonra başlat
    def delayed_rpa_start():
        print("🤖 RPA otomasyonu başlatılıyor...")
        rpa_bot.run(excel_files)

    gui_app.root.after(2000, delayed_rpa_start)

    # GUI'yi çalıştır
    gui_app.run()


def start_streamlit_server(port: int = 8501) -> subprocess.Popen:
    """Streamlit sunucusunu başlat"""
    print(f"🌐 Streamlit sunucusu başlatılıyor (Port: {port})...")

    try:
        process = subprocess.Popen([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port", str(port),
            "--server.headless", "true",
            "--server.enableCORS", "false"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print(f"✅ Streamlit başlatıldı: http://localhost:{port}")
        return process

    except Exception as e:
        print(f"❌ Streamlit başlatma hatası: {e}")
        return None



def run_rpa_with_gui(excel_paths: List[Path], progress_callback: Callable = None):
    """DÜZELTME: Streamlit entegrasyonu - Gelişmiş hata yönetimi"""
    global gui_app, rpa_bot, active_threads

    print(f"🎯 RPA işlemi başlatılıyor: {len(excel_paths)} dosya")

    def gui_worker():
        """DÜZELTME: GUI worker thread - hata yönetimi ile"""
        global gui_app
        try:
            from gui.base_gui import EnterpriseGUI
            gui_app = EnterpriseGUI()
            gui_app.set_processing_files(excel_paths)
            gui_app.run()
        except Exception as e:
            print(f"❌ GUI worker hatası: {e}")
        finally:
            print("🔄 GUI worker sonlandırıldı")

    # DÜZELTME: GUI thread'i daha güvenli başlat
    gui_thread = threading.Thread(target=gui_worker, daemon=True)
    gui_thread._stop_event = threading.Event()
    gui_thread.start()
    active_threads.append(gui_thread)

    # GUI'nin başlaması için bekle - timeout ile
    max_wait = 10
    for i in range(max_wait):
        if gui_app and hasattr(gui_app, 'root'):
            break
        time.sleep(1)
        print(f"⏳ GUI bekleniyor... ({i+1}/{max_wait})")

    if not gui_app:
        print("❌ GUI başlatılamadı - timeout")
        return []

    print("✅ GUI başlatıldı, RPA hazırlanıyor...")

    # DÜZELTME: RPA'yi ana thread'de çalıştır - hata yönetimi ile
    try:
        from rpa.core_engine import EnterpriseRPABot

        rpa_bot = EnterpriseRPABot()
        rpa_bot.set_gui_reference(gui_app)
        rpa_bot.set_processing_speed("normal")
        rpa_bot.set_processing_files(excel_paths)

        print("🚀 RPA başlatılıyor...")
        result = rpa_bot.run_complete_automation_sequence()
        print("✅ RPA tamamlandı!")

        if progress_callback:
            progress_callback(1.0, "Tüm dosyalar işlendi")

        return rpa_bot.get_results() if rpa_bot else []

    except Exception as e:
        print(f"❌ RPA Hatası: {e}")
        return []

    finally:
        # DÜZELTME: Güvenli temizlik
        print("🧹 RPA sonrası temizlik...")

        if gui_app and hasattr(gui_app, 'root'):
            try:
                gui_app.root.quit()
                gui_app.root.destroy()
            except:
                pass

        if gui_thread in active_threads:
            active_threads.remove(gui_thread)


def show_system_info():
    """Sistem bilgilerini göster"""
    print("\n" + "="*70)
    print("🔧 SİSTEM BİLGİLERİ")
    print("="*70)
    print("📋 KARMAŞIK RPA SİSTEMİ ÖZELLİKLERİ:")
    print("  🎯 4 Fazlı Enterprise Otomasyon:")
    print("     1️⃣ Karmaşık GUI Navigasyonu")
    print("     2️⃣ 6 Adımlı Süreç Yönetimi")  
    print("     3️⃣ Çoklu Excel Dosya İşleme")
    print("     4️⃣ Raporlama ve Sonlandırma")
    print("")
    print("  🖥️ Arayüz Seçenekleri:")
    print("     • Terminal Menü Sistemi")
    print("     • Streamlit Web Arayüzü (Drag & Drop)")
    print("     • Enterprise GUI (6 Modül + Alt Sekmeler)")
    print("")
    print("  🤖 RPA Yetenekleri:")
    print("     • Gerçekçi mouse hareketleri")
    print("     • POSH pattern filtreleme")
    print("     • Multi-threading desteği")
    print("     • 3 hız seviyesi (slow/normal/fast)")
    print("     • Detaylı logging ve hata yönetimi")
    print("")
    print("  📊 Raporlama:")
    print("     • Gerçek zamanlı progress tracking")
    print("     • Dosya bazında istatistikler")
    print("     • PDF rapor çıktısı")
    print("     • Dashboard güncellemeleri")
    print("="*70)


def show_demo_scenarios():
    """Demo senaryolarını göster"""
    print("\n" + "="*70)
    print("🎬 DEMO SENARYOLARI")
    print("="*70)
    print("1️⃣ Terminal Demo:")
    print("   • Seçenek 3: GUI + RPA birlikte")
    print("   • Karmaşık navigasyon gösterimi")
    print("   • Dashboard canlı güncelleme")
    print("")
    print("2️⃣ Streamlit Demo:")
    print("   • Web arayüzünde drag & drop")
    print("   • Çoklu dosya yükleme")
    print("   • RPA başlat butonu")
    print("   • Progress tracking")
    print("")
    print("3️⃣ Enterprise Demo:")
    print("   • 6 modüllü ERP sistemi")
    print("   • Alt sekme navigasyonu")
    print("   • 6 adımlı süreç akışı")
    print("   • Modal form sistemi")
    print("="*70)


def cleanup_resources():
    """DÜZELTME: Gelişmiş kaynak temizleme"""
    global gui_app, rpa_bot, active_threads, streamlit_process

    print("🧹 Sistem kaynakları temizleniyor...")

    # DÜZELTME: RPA'yi güvenli şekilde durdur
    if rpa_bot:
        try:
            rpa_bot.stop()
            print("✅ RPA bot durduruldu")
        except Exception as e:
            print(f"⚠️ RPA durdurma hatası: {e}")

    # DÜZELTME: GUI'yi güvenli şekilde kapat
    if gui_app and hasattr(gui_app, 'root'):
        try:
            gui_app.root.quit()
            gui_app.root.destroy()
            print("✅ GUI kapatıldı")
        except Exception as e:
            print(f"⚠️ GUI kapatma hatası: {e}")

    # DÜZELTME: Streamlit process'i güvenli şekilde kapat
    if streamlit_process:
        try:
            streamlit_process.terminate()
            streamlit_process.wait(timeout=5)
            print("✅ Streamlit process kapatıldı")
        except subprocess.TimeoutExpired:
            print("⚠️ Streamlit zorla kapatılıyor...")
            streamlit_process.kill()
        except Exception as e:
            print(f"⚠️ Streamlit kapatma hatası: {e}")

    # DÜZELTME: Aktif thread'leri gelişmiş şekilde sonlandır
    if active_threads:
        print(f"🔄 {len(active_threads)} thread sonlandırılıyor...")
        for i, thread in enumerate(active_threads):
            if thread.is_alive():
                print(f"⏳ Thread {i+1} bekleniyor...")
                thread.join(timeout=3)
                if thread.is_alive():
                    print(f"⚠️ Thread {i+1} hala aktif - zorla sonlandırılacak")
                    if hasattr(thread, '_stop_event'):
                        thread._stop_event.set()
                        thread.join(timeout=2)
                    if thread.is_alive():
                        print(f"❌ Thread {i+1} sonlandırılamadı")
                else:
                    print(f"✅ Thread {i+1} sonlandırıldı")

    # DÜZELTME: Global referansları temizle
    gui_app = None
    rpa_bot = None
    active_threads.clear()
    streamlit_process = None

    print("✅ Temizlik tamamlandı")

def signal_handler(signum, frame):
    """DÜZELTME: Signal handler - Ctrl+C için"""
    print(f"\n🛑 Signal {signum} alındı - temizlik yapılıyor...")
    cleanup_resources()
    sys.exit(0)

def setup_signal_handlers():
    """DÜZELTME: Signal handler'ları ayarla"""
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        atexit.register(cleanup_resources)
        print("✅ Signal handler'lar ayarlandı")
    except Exception as e:
        print(f"⚠️ Signal handler ayarlama hatası: {e}")


def main() -> None:
    """DÜZELTME: Ana fonksiyon - signal handler'lar ile"""
    try:
        # DÜZELTME: Signal handler'ları başlangıçta ayarla
        setup_signal_handlers()

        # Banner göster
        print_banner()

        # Komut satırı argümanlarını kontrol et
        args = parse_command_line_args()

        # Streamlit'ten gelen dosya işleme isteği varsa
        if args.files and len(args.files) > 0:
            print("📨 Streamlit entegrasyonu aktif")
            file_paths = [Path(f) for f in args.files]
            results = run_rpa_with_gui(file_paths)

            # Sonuçları JSON formatında yazdır (Streamlit için)
            import json
            print("RESULTS_JSON:", json.dumps(results))
            return

        # Komut satırından çalışma modu belirtildiyse etkileşimli menüyü atla
        if args.mode and args.mode != "terminal":
            if args.mode == "gui":
                start_gui_only()
            elif args.mode == "rpa":
                start_rpa_only()
            elif args.mode == "both":
                start_both_integrated()
            elif args.mode == "streamlit":
                streamlit_process = start_streamlit_server(args.port)
                if streamlit_process:
                    print(f"🌍 Tarayıcıda açın: http://localhost:{args.port}")
                    print("⏹️ Durdurmak için Ctrl+C basın")
                    try:
                        streamlit_process.wait()
                    except KeyboardInterrupt:
                        print("\n🛑 Streamlit durduruldu")
                        streamlit_process.terminate()
            return

        # Normal terminal menü modu
        while True:
            print("\n" + "="*70)
            print("🤖 KARMAŞIK RPA SİSTEMİ - ANA MENÜ")
            print("="*70)
            print("1️⃣ 🖥️  Sadece Enterprise GUI'yi başlat")
            print("2️⃣ 🤖 RPA bot'unu çalıştır (GUI açık olmalı)")  
            print("3️⃣ 🚀 GUI + RPA entegre başlat (DEMO MOD)")
            print("4️⃣ 🌐 Streamlit web arayüzünü başlat")
            print("5️⃣ 📋 Sistem bilgilerini göster")
            print("6️⃣ 🎬 Demo senaryolarını göster")
            print("0️⃣ ❌ Çıkış")
            print("="*70)

            try:
                choice = input("🎯 Seçiminiz (0-6): ").strip()

                if choice == "1":
                    print("🖥️ Enterprise GUI başlatılıyor...")
                    start_gui_only()

                elif choice == "2":
                    print("🤖 RPA bot'u çalıştırılıyor...")
                    start_rpa_only()

                elif choice == "3":
                    print("🚀 Entegre sistem başlatılıyor...")
                    start_both_integrated()

                elif choice == "4":
                    print("🌐 Streamlit başlatılıyor...")
                    streamlit_process = start_streamlit_server(args.port)
                    if streamlit_process:
                        print(f"🌍 Tarayıcıda açın: http://localhost:{args.port}")
                        print("⏹️ Durdurmak için Ctrl+C basın")
                        try:
                            streamlit_process.wait()
                        except KeyboardInterrupt:
                            print("\n🛑 Streamlit durduruldu")
                            streamlit_process.terminate()

                elif choice == "5":
                    show_system_info()

                elif choice == "6":
                    show_demo_scenarios()

                elif choice == "0":
                    print("👋 Sistem kapatılıyor...")
                    cleanup_resources()
                    print("✅ Güle güle!")
                    break

                else:
                    print("❌ Geçersiz seçim! Lütfen 0-6 arası bir sayı girin.")

            except KeyboardInterrupt:
                print("\n\n⚠️ Kullanıcı tarafından iptal edildi")
                cleanup_resources()
                break
            except Exception as e:
                print(f"❌ Beklenmeyen hata: {e}")
                continue

    except Exception as e:
        print(f"💥 Kritik sistem hatası: {e}")
    finally:
        cleanup_resources()


if __name__ == "__main__":
    main()

