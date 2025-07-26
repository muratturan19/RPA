"""
Karmaşık RPA Motoru - Enterprise Seviye Otomasyon
Çoklu Excel dosya işleme + 6 adımlı karmaşık GUI navigasyonu
"""
import time
import threading
import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional
import tkinter as tk
import pyautogui
import random
from datetime import datetime

class EnterpriseRPABot:
    """Enterprise seviye RPA botu - Karmaşık navigasyon ve çoklu dosya işleme"""
    
    def __init__(self):
        self.gui = None
        self.is_running = False
        self.excel_files = []
        self.current_file_index = 0
        self.all_excel_data = {}  # Dosya bazında veri
        self.current_record_index = 0
        self.total_records_processed = 0
        self.failed_records = 0
        
        # Performans ayarları
        self.processing_speed = "fast"  # "slow", "normal", "fast"
        # Tüm beklemeleri yarıya indirmek için katsayı
        self.delay_factor = 0.5
        self.mouse_simulation = True
        self.detailed_logging = True
        
        # RPA istatistikleri
        self.start_time = None
        self.results = []
        
    def set_gui_reference(self, gui_app):
        """GUI referansını ayarla"""
        self.gui = gui_app
        self.log_step("✅ Enterprise GUI referansı ayarlandı", 0.3)
        
    def set_processing_files(self, file_paths: List[Path]):
        """İşlenecek dosya listesini ayarla"""
        self.excel_files = file_paths
        self.log_step(f"📁 {len(file_paths)} Excel dosyası işlenmeye hazırlandı", 0.5)
        
    def set_processing_speed(self, speed: str):
        """İşlem hızını ayarla: slow, normal, fast"""
        self.processing_speed = speed
        self.log_step(f"⚡ İşlem hızı: {speed}", 0.2)
        
    def log_step(self, message: str, delay: float = 0.5):
        """Adımları logla ve bekle"""
        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        if self.detailed_logging:
            print(f"[{timestamp}] [RPA] {message}")
        
        if self.gui:
            self.call_in_gui_thread(self.gui.update_status, f"RPA: {message}")
            
        # Hız ayarına göre bekleme
        speed_multiplier = {"slow": 2.0, "normal": 1.0, "fast": 0.3}
        actual_delay = delay * speed_multiplier.get(self.processing_speed, 1.0) * self.delay_factor
        time.sleep(actual_delay)

    def call_in_gui_thread(self, func, *args, **kwargs):
        """Tkinter ana döngüsünde güvenli fonksiyon çalıştırma"""
        if not self.gui or not hasattr(self.gui, 'root'):
            return
            
        done = threading.Event()
        result = None
        exception = None

        def wrapper():
            nonlocal result, exception
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                exception = e
            finally:
                done.set()

        self.gui.root.after(0, wrapper)
        done.wait(timeout=5.0)  # 5 saniye timeout
        
        if exception:
            self.log_step(f"⚠️ GUI thread hatası: {exception}", 0.1)
        return result

    def focus_window(self):
        """GUI penceresini öne getir"""
        if self.gui and hasattr(self.gui, 'root'):
            self.gui.root.lift()
            self.gui.root.attributes('-topmost', True)
            self.gui.root.after(100, lambda: self.gui.root.attributes('-topmost', False))
            self.gui.root.focus_force()

    def highlight_widget(self, widget, flash_ms: int = 150):
        """Kısa bir highlight efekti uygula"""
        try:
            orig_bg = widget.cget('highlightbackground')
            orig_thick = widget.cget('highlightthickness')
            widget.configure(highlightbackground='red', highlightthickness=2)
            widget.after(flash_ms, lambda: widget.configure(highlightbackground=orig_bg, highlightthickness=orig_thick))
        except Exception:
            pass

    class _BBoxWidget:
        """Notebook sekmeleri için sanal widget"""

        def __init__(self, x: int, y: int, w: int, h: int):
            self._x = x
            self._y = y
            self._w = w
            self._h = h

        def winfo_rootx(self):
            return self._x

        def winfo_rooty(self):
            return self._y

        def winfo_width(self):
            return self._w

        def winfo_height(self):
            return self._h

    def get_tab_widget(self, index: int):
        """Notebook sekme koordinatlarından sanal widget döndür"""
        if not self.gui or not hasattr(self.gui, "notebook"):
            return None
        try:
            bbox = self.gui.notebook.bbox(index)
            if not bbox:
                return None
            x, y, w, h = bbox
            rootx = self.gui.notebook.winfo_rootx() + x
            rooty = self.gui.notebook.winfo_rooty() + y
            return self._BBoxWidget(rootx, rooty, w, h)
        except Exception:
            return None
        
    def move_mouse_to_widget(self, widget, smooth: bool = True):
        """Fareyi widget'a yumuşak hareketle taşı"""
        if not self.mouse_simulation:
            return

        try:
            self.focus_window()
            # Widget koordinatlarını al
            x = widget.winfo_rootx() + widget.winfo_width() // 2
            y = widget.winfo_rooty() + widget.winfo_height() // 2
            
            # Küçük rastgele offset (daha doğal)
            x += random.randint(-5, 5)
            y += random.randint(-2, 2)
            
            # Yumuşak hareket
            duration = 0.3 if smooth else 0.1
            pyautogui.moveTo(x, y, duration=duration)
            
            # Çok kısa bekleme (gerçekçi)
            time.sleep(random.uniform(0.05, 0.15) * self.delay_factor)
            
        except Exception as e:
            self.log_step(f"⚠️ Mouse hareket hatası: {e}", 0.1)
            
    def click_widget_simulation(self, widget_name: str, widget=None, delay: float = 0.5):
        """Widget tıklama simülasyonu - gelişmiş"""
        self.log_step(f"🖱️ {widget_name} tıklanıyor...", 0.2)

        if widget and self.mouse_simulation:
            self.call_in_gui_thread(self.move_mouse_to_widget, widget, True)
            self.call_in_gui_thread(self.highlight_widget, widget)

        # Tıklama gecikmesi
        time.sleep(random.uniform(0.1, 0.3) * self.delay_factor)
        self.log_step(f"✅ {widget_name} başarıyla tıklandı", delay)
        
    # === PHASE 1: KARMAŞIK GUI NAVİGASYONU ===
    
    def phase1_navigate_to_finance_module(self):
        """1. Faz: Finans modülüne karmaşık navigasyon"""
        self.log_step("🎯 FAZ 1: Finans-Tahsilat modülüne navigasyon başlıyor...", 1.0)

        # Pencereyi öne getir ve mouse hareketlerini göster
        self.call_in_gui_thread(self.focus_window)

        tab_keys = {
            0: "dashboard",
            1: "accounting",
            2: "finance",
            3: "inventory",
            4: "reports",
            5: "system",
        }

        # 0 - Dashboard sekmesine tıkla
        dashboard_widget = self.get_tab_widget(0)
        self.click_widget_simulation("Dashboard sekmesi", dashboard_widget)
        self.call_in_gui_thread(self.gui.notebook.select, 0)

        # Sırayla Muhasebe(1), Stok(3), Raporlar(4), Sistem(5)
        sequence = [
            (1, "Muhasebe"),
            (3, "Stok"),
            (4, "Raporlar"),
            (5, "Sistem"),
        ]

        for idx, name in sequence:
            widget = self.get_tab_widget(idx)
            self.click_widget_simulation(f"{name} sekmesi", widget)
            self.call_in_gui_thread(self.gui.notebook.select, idx)

        # Son olarak Finans-Tahsilat(2)
        finance_widget = self.get_tab_widget(2)
        self.click_widget_simulation("Finans-Tahsilat sekmesi", finance_widget)
        self.call_in_gui_thread(self.gui.notebook.select, 2)

        # Veri Giriş modal'ını aç
        self.log_step("🚀 Veri Giriş modal'ı açılıyor...", 0.8)
        self.call_in_gui_thread(self.gui.open_advanced_data_entry)
        self.log_step("⏳ Modal yükleniyor...", 1.0)

        # Dashboard sekmesine geri dön (modal açık kalsın)
        self.log_step("↩️ Dashboard sekmesine dönülüyor (modal açık)...", 0.5)
        self.click_widget_simulation("Dashboard sekmesi", dashboard_widget)
        self.call_in_gui_thread(self.gui.notebook.select, 0)

        # Veri girişi başlat
        self.log_step("🚀 Veri girişi başlatılıyor...", 0.5)

        self.log_step("✅ FAZ 1 TAMAMLANDI: Navigasyon ve modal hazır", 1.0)
        
    def phase2_execute_6_step_process(self):
        """2. Faz: 6 adımlı süreç navigasyonu"""
        self.log_step("🎯 FAZ 2: 6 Adımlı Veri İşlem Süreci başlıyor...", 1.0)
        
        # Bu adımları sırayla çalıştır
        steps = [
            ("1️⃣ Veri Kaynağı Seçimi", self.execute_step1_source_selection),
            ("2️⃣ Kayıt Filtreleme", self.execute_step2_record_filtering),
            ("3️⃣ Veri Önizleme", self.execute_step3_data_preview),
            ("4️⃣ İşlem Parametreleri", self.execute_step4_parameters),
            ("5️⃣ Veri Giriş Başlatma", self.execute_step5_data_entry),
            ("6️⃣ Toplu Onay İşlemi", self.execute_step6_batch_confirm)
        ]
        
        for step_name, step_function in steps:
            self.log_step(f"🔄 {step_name} çalıştırılıyor...", 0.5)
            step_function()
            self.log_step(f"✅ {step_name} tamamlandı", 0.8)
            
        self.log_step("✅ FAZ 2 TAMAMLANDI: 6 adımlı süreç bitti", 1.5)
        
    def execute_step1_source_selection(self):
        """Adım 1: Veri kaynağı seçimi"""
        self.call_in_gui_thread(self.gui.step1_select_source)
        
    def execute_step2_record_filtering(self):
        """Adım 2: Kayıt filtreleme"""
        self.call_in_gui_thread(self.gui.step2_filter_records)
        
    def execute_step3_data_preview(self):
        """Adım 3: Veri önizleme"""
        self.call_in_gui_thread(self.gui.step3_preview_data)
        
    def execute_step4_parameters(self):
        """Adım 4: İşlem parametreleri"""
        self.call_in_gui_thread(self.gui.step4_set_parameters)
        
    def execute_step5_data_entry(self):
        """Adım 5: Veri giriş başlatma - MODAL AÇMA"""
        self.log_step("🚀 Kritik Adım: Veri Giriş Modal'ı açılıyor...", 1.0)
        if hasattr(self.gui, 'finans_frame'):
            self.call_in_gui_thread(self.highlight_widget, self.gui.finans_frame)
        self.call_in_gui_thread(self.gui.step5_start_data_entry)
        
        # Modal'ın açılması için bekle
        self.log_step("⏳ Veri Giriş Modal'ının yüklenmesi bekleniyor...", 2.0)
        
    def execute_step6_batch_confirm(self):
        """Adım 6: Toplu onay (işlem sonunda)"""
        # Bu adım veri işleme bittikten sonra çalışacak
        pass
        
    # === PHASE 3: ÇOKLU EXCEL İŞLEME ===
    
    def phase3_process_multiple_excel_files(self):
        """3. Faz: Çoklu Excel dosya işleme"""
        self.log_step("🎯 FAZ 3: Çoklu Excel dosya işleme başlıyor...", 1.0)
        
        if not self.excel_files:
            self.log_step("⚠️ İşlenecek Excel dosyası bulunamadı!", 1.0)
            return
            
        total_files = len(self.excel_files)
        self.log_step(f"📊 Toplam {total_files} Excel dosyası işlenecek", 1.0)
        
        # Her dosyayı sırayla işle
        for file_index, excel_path in enumerate(self.excel_files, 1):
            self.current_file_index = file_index - 1
            self.log_step(f"📄 Dosya {file_index}/{total_files}: {excel_path.name}", 1.0)
            
            # Dosyayı yükle ve işle
            success = self.process_single_excel_file(excel_path)
            
            if success:
                self.log_step(f"✅ Dosya {file_index} başarıyla tamamlandı", 1.0)
            else:
                self.log_step(f"❌ Dosya {file_index} işlenirken hata oluştu", 1.0)
                
            # Dosyalar arası bekleme
            if file_index < total_files:
                self.log_step(f"⏳ Sonraki dosyaya geçiliyor... ({file_index + 1}/{total_files})", 1.5)
                
        self.log_step("✅ FAZ 3 TAMAMLANDI: Tüm Excel dosyaları işlendi", 2.0)
        
    def process_single_excel_file(self, excel_path: Path) -> bool:
        """Tek Excel dosyasını işle"""
        try:
            self.log_step(f"📂 Excel dosyası okunuyor: {excel_path.name}", 0.8)
            
            # Excel'i oku
            raw_data = pd.read_excel(excel_path, header=23)  # 23. satırdan başla
            
            # POSH pattern filtresi
            pattern = r'^POSH.*\/\d{15}$'
            aciklama_cols = [col for col in raw_data.columns if 'açıklama' in str(col).lower()]
            
            if not aciklama_cols:
                self.log_step("⚠️ Açıklama sütunu bulunamadı, varsayılan sütun kullanılıyor", 0.5)
                aciklama_col = raw_data.columns[2]
            else:
                aciklama_col = aciklama_cols[0]
                
            # Filtreleme
            filtered_data = raw_data[raw_data[aciklama_col].astype(str).str.match(pattern, na=False)]
            
            # Veriyi işlenebilir formata çevir
            processed_records = []
            for _, row in filtered_data.iterrows():
                record = {
                    'tarih': str(row.iloc[0]) if len(row) > 0 else datetime.now().strftime('%d.%m.%Y'),
                    'aciklama': str(row[aciklama_col]) if pd.notna(row[aciklama_col]) else "",
                    'tutar': str(row.iloc[3]) if len(row) > 3 else "0",
                    'dosya': excel_path.name
                }
                processed_records.append(record)
                
            # Dosya bazında veriyi sakla
            self.all_excel_data[excel_path.name] = processed_records
            
            self.log_step(f"🔍 {len(processed_records)} geçerli kayıt bulundu", 0.8)
            
            # Kayıtları GUI'ye aktar
            if self.gui:
                self.call_in_gui_thread(self.gui.set_current_records, processed_records)
                
            # Her kayıt için veri girişi yap
            self.process_records_from_file(processed_records, excel_path.name)
            
            # Dosya sonucu kaydet
            self.results.append({
                'file': excel_path.name,
                'records': len(processed_records),
                'success': len(processed_records) - self.failed_records,
                'errors': self.failed_records,
                'processing_time': time.time() - self.start_time if self.start_time else 0
            })
            
            return True
            
        except Exception as e:
            self.log_step(f"❌ Excel işleme hatası: {e}", 1.0)
            
            # Hata sonucu kaydet
            self.results.append({
                'file': excel_path.name,
                'records': 0,
                'success': 0,
                'errors': 1,
                'error_message': str(e)
            })
            return False
            
    def process_records_from_file(self, records: List[Dict], file_name: str):
        """Dosyadan gelen kayıtları tek tek işle"""
        total_records = len(records)
        self.log_step(f"📝 {file_name} dosyasından {total_records} kayıt işlenecek", 1.0)
        
        for record_index, record in enumerate(records, 1):
            self.log_step(f"📋 Kayıt {record_index}/{total_records}: {record['aciklama'][:50]}...", 0.3)
            
            # Tek kaydı işle
            success = self.process_single_record(record, record_index, total_records)
            
            if success:
                self.total_records_processed += 1
            else:
                self.failed_records += 1
                
            # Kayıtlar arası kısa bekleme
            time.sleep(random.uniform(0.2, 0.5) * self.delay_factor)
            
        self.log_step(f"✅ {file_name} dosyasının tüm kayıtları işlendi", 1.0)
        
    def process_single_record(self, record: Dict, record_num: int, total: int) -> bool:
        """Tek kayıt işleme - Modal form doldurma"""
        try:
            # Form alanlarını doldur
            if not self.gui or not hasattr(self.gui, 'modal_entries'):
                self.log_step("⚠️ Modal form bulunamadı, kayıt atlanıyor", 0.5)
                return False
                
            entries = self.gui.modal_entries
            
            # 1. Tarih alanı
            self.log_step(f"📅 Tarih giriliyor: {record['tarih']}", 0.3)
            self.click_widget_simulation("Tarih alanı", entries.get('date_entry'))
            self.call_in_gui_thread(self.fill_entry_field, entries['date_entry'], record['tarih'])
            
            # 2. Açıklama alanı
            short_desc = record['aciklama'][:80] + "..." if len(record['aciklama']) > 80 else record['aciklama']
            self.log_step(f"📝 Açıklama giriliyor: {short_desc[:30]}...", 0.3)
            self.click_widget_simulation("Açıklama alanı", entries.get('desc_entry'))
            self.call_in_gui_thread(self.fill_entry_field, entries['desc_entry'], short_desc)
            
            # 3. Tutar alanı
            self.log_step(f"💰 Tutar giriliyor: {record['tutar']}", 0.3)
            self.click_widget_simulation("Tutar alanı", entries.get('amount_entry'))
            self.call_in_gui_thread(self.fill_entry_field, entries['amount_entry'], record['tutar'])
            
            # 4. Dosya alanı
            self.log_step(f"📁 Dosya adı giriliyor: {record['dosya']}", 0.3)
            self.click_widget_simulation("Dosya alanı", entries.get('file_entry'))
            self.call_in_gui_thread(self.fill_entry_field, entries['file_entry'], record['dosya'])
            
            # 5. Kaydet butonu
            self.log_step("💾 Kayıt kaydediliyor...", 0.5)
            self.click_widget_simulation("Kaydet butonu")
            self.call_in_gui_thread(self.gui.save_advanced_record)
            
            self.log_step(f"✅ Kayıt {record_num}/{total} başarıyla işlendi", 0.8)
            return True
            
        except Exception as e:
            self.log_step(f"❌ Kayıt işleme hatası: {e}", 0.5)
            return False
            
    def fill_entry_field(self, entry_widget, value: str):
        """Entry alanını güvenli şekilde doldur"""
        try:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, value)
        except Exception as e:
            self.log_step(f"⚠️ Alan doldurma hatası: {e}", 0.1)
            
    # === PHASE 4: FİNALİZASYON ===
    
    def phase4_finalization_and_reports(self):
        """4. Faz: Sonlandırma ve raporlama"""
        self.log_step("🎯 FAZ 4: Sonlandırma ve raporlama...", 1.0)
        
        # 6. adımı çalıştır (toplu onay)
        self.log_step("✅ Adım 6: Toplu onay işlemi gerçekleştiriliyor...", 1.0)
        self.call_in_gui_thread(self.gui.step6_batch_confirm)
        
        # İstatistikleri hesapla
        total_files = len(self.excel_files)
        total_records = self.total_records_processed
        success_rate = (total_records / (total_records + self.failed_records) * 100) if (total_records + self.failed_records) > 0 else 0
        processing_time = time.time() - self.start_time if self.start_time else 0
        
        # Sonuç raporu
        self.log_step("📊 SONUÇ RAPORU:", 1.0)
        self.log_step(f"   📁 İşlenen Dosya Sayısı: {total_files}", 0.3)
        self.log_step(f"   📋 Toplam Kayıt Sayısı: {total_records}", 0.3)
        self.log_step(f"   ✅ Başarılı İşlemler: {total_records}", 0.3)
        self.log_step(f"   ❌ Başarısız İşlemler: {self.failed_records}", 0.3)
        self.log_step(f"   📈 Başarı Oranı: %{success_rate:.1f}", 0.3)
        self.log_step(f"   ⏱️ Toplam Süre: {processing_time:.1f} saniye", 0.3)
        
        self.log_step("✅ FAZ 4 TAMAMLANDI: Tüm işlemler bitti", 2.0)
        
    # === ANA RPA SÜREÇ YÖNETİMİ ===
    
    def run_complete_automation_sequence(self):
        """Tam otomasyon sekansı - 4 fazlı süreç"""
        try:
            self.start_time = time.time()
            self.log_step("🚀 KARMAŞIK RPA SİSTEMİ BAŞLATILUYOR...", 2.0)
            self.log_step("🎯 Enterprise seviye otomasyon - 4 fazlı süreç", 1.0)
            
            # FAZ 1: GUI Navigasyonu
            self.phase1_navigate_to_finance_module()
            
            # FAZ 2: 6 Adımlı Süreç
            self.phase2_execute_6_step_process()
            
            # FAZ 3: Çoklu Excel İşleme
            self.phase3_process_multiple_excel_files()
            
            # FAZ 4: Sonlandırma
            self.phase4_finalization_and_reports()
            
            # Genel başarı mesajı
            self.log_step("🎉 KARMAŞIK RPA SİSTEMİ BAŞARIYLA TAMAMLANDI!", 2.0)
            self.log_step("📊 Tüm fazlar ve dosyalar işlendi", 1.0)
            
        except Exception as e:
            self.log_step(f"❌ KRITIK RPA SISTEMI HATASI: {e}", 2.0)
        finally:
            self.is_running = False
            
    def run(self, excel_files: List[Path] = None, progress_callback: Callable = None):
        """RPA'yi başlat - Ana giriş noktası"""
        if not self.gui:
            self.log_step("❌ GUI referansı ayarlanmamış!", 1.0)
            return None
            
        if excel_files:
            self.set_processing_files(excel_files)
            
        self.is_running = True
        self.progress_callback = progress_callback
        
        def automation_worker():
            try:
                self.run_complete_automation_sequence()
                
                # Progress callback ile sonucu bildir
                if self.progress_callback:
                    self.progress_callback(1.0, "Tüm dosyalar işlendi")
                    
            except Exception as e:
                self.log_step(f"❌ RPA Worker Hatası: {e}", 1.0)
            finally:
                self.is_running = False
                
        thread = threading.Thread(target=automation_worker, daemon=True)
        thread.start()
        return thread
        
    def get_results(self) -> List[Dict[str, Any]]:
        """İşlem sonuçlarını döndür"""
        return self.results
        
    def stop(self):
        """RPA'yi durdur"""
        self.is_running = False
        self.log_step("🛑 RPA sistemi durduruldu", 1.0)

# Test fonksiyonu
if __name__ == "__main__":
    print("🤖 Karmaşık RPA Motoru - Test Modu")
    bot = EnterpriseRPABot()
    bot.set_processing_speed("fast")
    print("✅ RPA motoru hazır")
