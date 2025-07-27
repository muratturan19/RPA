import time
import threading
import pandas as pd
from pathlib import Path
import tkinter as tk
import pyautogui

class AdvancedRPABot:
    """Gerçekçi RPA botu - Presto benzeri akış"""
    
    def __init__(self):
        self.gui = None
        self.is_running = False
        self.excel_data = []
        self.current_record_index = 0
        
    def set_gui_reference(self, gui_app):
        """GUI referansını ayarla"""
        self.gui = gui_app
        print("✅ GUI referansı ayarlandı")
        
    def log_step(self, message, delay=0.5):
        """Adımları logla ve bekle"""
        print(f"[RPA] {message}")
        if self.gui:
            self.gui.update_status(f"RPA: {message}")
        time.sleep(delay)

    def call_in_gui_thread(self, func, *args, timeout=None, **kwargs):
        """Tkinter ana döngüsünde fonksiyon çalıştır"""
        if not self.gui:
            return
        done = threading.Event()

        def wrapper():
            try:
                func(*args, **kwargs)
            finally:
                done.set()

        self.gui.root.after(0, wrapper)
        done.wait(timeout)
        
    def click_simulation(self, widget_name, delay=0.5):
        """Widget tıklama simülasyonu"""
        self.log_step(f"🖱️ {widget_name} tıklanıyor...", 0.25)

        widget = None
        if self.gui:
            if widget_name == "Tarih alanı":
                widget = self.gui.date_entry
            elif widget_name == "Açıklama alanı":
                widget = self.gui.desc_entry
            elif widget_name == "Tutar alanı":
                widget = self.gui.amount_entry
            elif widget_name == "Kaydet butonu":
                widget = self.gui.save_btn

        if widget is not None:
            self.call_in_gui_thread(self.move_mouse_to_widget, widget)

        time.sleep(delay)
        self.log_step(f"✅ {widget_name} tıklandı", 0.25)

    def move_mouse_to_widget(self, widget):
        """Fareyi belirtilen widget'ın ortasına taşı"""
        try:
            x = widget.winfo_rootx() + widget.winfo_width() // 2
            y = widget.winfo_rooty() + widget.winfo_height() // 2
            pyautogui.moveTo(x, y, duration=0.3)
        except Exception as exc:
            print(f"Mouse move error: {exc}")
        
    def navigate_to_finans_tab(self):
        """Finans-Tahsilat sekmesine git"""
        self.log_step("📊 Finans-Tahsilat sekmesine geçiliyor...", 1)

        # GUI'de sekmeye geç
        self.call_in_gui_thread(self.gui.notebook.select, 1)
        self.log_step("✅ Finans-Tahsilat sekmesi açıldı", 0.5)
        
    def click_data_entry_button(self):
        """Veri Giriş butonuna tıkla"""
        self.log_step("📋 Üstteki 'Veri Giriş' butonuna tıklanıyor...", 1)

        # Veri Giriş modal'ını aç
        self.call_in_gui_thread(self.gui.open_data_entry)
        self.log_step("✅ Veri Giriş penceresi açıldı", 1)
        
    def load_excel_data(self):
        """Excel'den veri yükle"""
        self.log_step("📂 Excel dosyasından veriler okunuyor...", 1)
        
        try:
            # Excel dosyasını bul
            excel_path = Path("../data/Vadesiz_Hesap_Detay.xlsx")
            if not excel_path.exists():
                excel_path = Path("data/Vadesiz_Hesap_Detay.xlsx")
                
            if excel_path.exists():
                # Excel'i header satırından oku
                raw_data = pd.read_excel(excel_path, header=23)
                
                # POSH pattern'i ile filtrele
                pattern = r'^POSH.*\/\d{15}$'
                
                # Açıklama sütununu bul
                aciklama_cols = [col for col in raw_data.columns if 'açıklama' in str(col).lower()]
                if aciklama_cols:
                    aciklama_col = aciklama_cols[0]
                    filtered_data = raw_data[raw_data[aciklama_col].astype(str).str.match(pattern, na=False)]
                    
                    # Veriyi işle
                    for _, row in filtered_data.iterrows():
                        tarih = str(row.iloc[0]) if len(row) > 0 else ""
                        aciklama = str(row[aciklama_col]) if pd.notna(row[aciklama_col]) else ""
                        tutar = str(row.iloc[3]) if len(row) > 3 else "0"
                        
                        self.excel_data.append({
                            'tarih': tarih,
                            'aciklama': aciklama,
                            'tutar': tutar
                        })
                        
                    self.log_step(f"✅ {len(self.excel_data)} adet geçerli kayıt bulundu", 0.5)
                    return True
                    
            # Excel bulunamazsa test verisi oluştur
            self.create_test_data()
            return True
            
        except Exception as e:
            self.log_step(f"❌ Excel okuma hatası: {e}", 0.5)
            self.create_test_data()
            return True
            
    def create_test_data(self):
        """Test verisi oluştur"""
        self.log_step("🧪 Test verisi oluşturuluyor...", 0.5)
        
        test_records = [
            {"tarih": "23.07.2025", "aciklama": "POSH/20250723/000000002391280/N042 K P POS Satış /000001660659421", "tutar": "670.99"},
            {"tarih": "23.07.2025", "aciklama": "POSH/20250723/000000002391280/N042 K P ÜİY Komisyon /000001660659421", "tutar": "-13.42"},
            {"tarih": "23.07.2025", "aciklama": "POSH/20250723/000000002391280/TY01 N P POS Satış /000001660659422", "tutar": "307.49"},
            {"tarih": "23.07.2025", "aciklama": "POSH/20250723/000000002391280/TY01 N P ÜİY Komisyon /000001660659422", "tutar": "-8.46"},
            {"tarih": "24.07.2025", "aciklama": "POSH/20250724/000000002391280/N001 N P POS Satış /000001661601485", "tutar": "4559.47"},
        ]
        
        self.excel_data = test_records
        self.log_step(f"✅ {len(self.excel_data)} test kaydı hazırlandı", 0.5)
        
    def process_single_record(self, record):
        """Tek kaydı işle - Form doldur ve kaydet"""
        self.log_step(f"📝 Kayıt işleniyor: {record['aciklama'][:50]}...", 0.5)
        
        # 1. Tarih alanına tıkla ve veri gir
        self.click_simulation("Tarih alanı")
        self.call_in_gui_thread(self.gui.date_entry.delete, 0, tk.END)
        self.call_in_gui_thread(self.gui.date_entry.insert, 0, record['tarih'])
        self.log_step(f"📅 Tarih girildi: {record['tarih']}", 0.5)
        
        # 2. Açıklama alanına tıkla ve veri gir
        self.click_simulation("Açıklama alanı")
        self.call_in_gui_thread(self.gui.desc_entry.delete, 0, tk.END)
        
        # Açıklamayı kısalt
        short_desc = record['aciklama'][:80] + "..." if len(record['aciklama']) > 80 else record['aciklama']
        self.call_in_gui_thread(self.gui.desc_entry.insert, 0, short_desc)
        self.log_step(f"📝 Açıklama girildi: {short_desc[:30]}...", 0.5)
        
        # 3. Tutar alanına tıkla ve veri gir
        self.click_simulation("Tutar alanı")
        self.call_in_gui_thread(self.gui.amount_entry.delete, 0, tk.END)
        self.call_in_gui_thread(self.gui.amount_entry.insert, 0, record['tutar'])
        self.log_step(f"💰 Tutar girildi: {record['tutar']} TL", 0.5)
        
        # 4. Kaydet butonuna tıkla
        self.click_simulation("Kaydet butonu", 1)
        self.call_in_gui_thread(self.gui.save_current_record)
        self.log_step("✅ Kayıt başarıyla kaydedildi", 0.5)
        
        # 5. Kısa bekleme
        self.log_step("⏳ Sonraki kayıt için hazırlanıyor...", 0.75)
        
    def run_automation_sequence(self):
        """Ana otomasyon sekansı"""
        self.log_step("🤖 RPA Otomasyonu başlatılıyor...", 1)
        
        try:
            # 1. Finans sekmesine git
            self.navigate_to_finans_tab()
            
            # 2. Veri Giriş butonuna tıkla
            self.click_data_entry_button()
            
            # 3. Excel verilerini yükle
            if not self.load_excel_data():
                self.log_step("❌ Veri yüklenemedi, işlem durduruluyor", 0.5)
                return

            # GUI'ye veriyi ata ve önizleme için göster
            if self.gui is not None:
                try:
                    self.call_in_gui_thread(
                        self.gui.set_current_records, list(self.excel_data)
                    )
                    if hasattr(self.gui, "show_data"):
                        self.call_in_gui_thread(self.gui.show_data)
                except Exception as exc:
                    self.log_step(f"❌ GUI gosterim hatasi: {exc}", 0.5)
                
            # 4. Her kayıt için döngü
            total_records = len(self.excel_data)
            self.log_step(f"🔄 {total_records} kayıt işlenecek", 1)
            
            for i, record in enumerate(self.excel_data, 1):
                self.log_step(f"--- İŞLEM {i}/{total_records} ---", 0.5)
                
                # Kaydı işle
                self.process_single_record(record)
                
                # İlerleme raporu
                if i % 5 == 0:
                    self.log_step(f"📊 İlerleme: {i}/{total_records} kayıt tamamlandı", 0.5)
                    
            # Tamamlandı
            self.log_step("🎉 TÜM KAYITLAR BAŞARIYLA İŞLENDİ!", 1.5)
            self.log_step(f"📈 Sonuç: {total_records} kayıt ana tabloya eklendi", 0.5)
            
        except Exception as e:
            self.log_step(f"❌ RPA Sistemi Hatası: {e}", 0.5)
            
    def run(self):
        """RPA'yi threading ile çalıştır"""
        if not self.gui:
            print("❌ GUI referansı ayarlanmamış!")
            return
            
        self.is_running = True
        
        def automation_worker():
            try:
                self.run_automation_sequence()
            except Exception as e:
                self.log_step(f"❌ RPA Sistemi Hatası: {e}")
            finally:
                self.is_running = False
                
        thread = threading.Thread(target=automation_worker, daemon=True)
        thread.start()
        return thread

    def stop(self):
        """RPA'yi durdur"""
        self.is_running = False
        print("🛑 RPA sistemi durduruldu")
