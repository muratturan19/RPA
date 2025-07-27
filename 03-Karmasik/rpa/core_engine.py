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

# DÜZELTME: PyAutoGUI güvenlik ayarları
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

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
        """DÜZELTME: Tkinter ana döngüsünde güvenli fonksiyon çalıştırma"""
        if not self.gui or not hasattr(self.gui, 'root'):
            self.log_step("⚠️ GUI referansı mevcut değil", 0.1)
            return None

        # DÜZELTME: Root window kontrolü
        try:
            self.gui.root.winfo_exists()
        except tk.TclError:
            self.log_step("⚠️ Ana pencere mevcut değil", 0.1)
            return None

        # DÜZELTME: Widget varlık kontrolü - daha güvenli
        if args:
            for arg in args:
                if hasattr(arg, 'winfo_exists'):
                    try:
                        if not arg.winfo_exists():
                            self.log_step("⚠️ Widget artık mevcut değil", 0.1)
                            return None
                    except (tk.TclError, AttributeError):
                        self.log_step("⚠️ Widget kontrol hatası", 0.1)
                        return None

        done = threading.Event()
        result = None
        exception = None

        def wrapper():
            nonlocal result, exception
            try:
                result = func(*args, **kwargs)
            except tk.TclError as e:
                exception = f"TclError: {e}"
            except Exception as e:
                exception = f"Genel Hata: {e}"
            finally:
                done.set()

        try:
            self.gui.root.after(0, wrapper)
            # DÜZELTME: Timeout ile bekle - sonsuz bekleme önlenir
            # ZAMAN AŞIMI 60 SANİYEYE ÇIKARILDI
            if done.wait(timeout=60):  # 60 saniye timeout
                if exception:
                    self.log_step(f"⚠️ GUI thread hatası: {exception}", 0.1)
                return result
            else:
                self.log_step("⚠️ GUI thread 60s timeout", 0.1)
                return None
        except tk.TclError:
            self.log_step("⚠️ GUI thread çağırma hatası", 0.1)
            return None

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

    def after_mouse_click(self):
        """Mouse tıklamasından sonra modal'ı tekrar öne getir."""
        if self.gui and getattr(self.gui, 'data_entry_window', None):
            try:
                self.gui.data_entry_window.lift()
                self.gui.data_entry_window.focus_force()
            except Exception:
                pass

    def _is_popup_open(self) -> bool:
        """Pop-up açık mı kontrol et"""
        try:
            if not self.gui or not hasattr(self.gui, 'root'):
                return False

            for widget in self.gui.root.winfo_children():
                if isinstance(widget, tk.Toplevel):
                    try:
                        widget.winfo_exists()
                        return True
                    except tk.TclError:
                        continue
            return False
        except Exception:
            return False

    def wait_for_modal_ready(self, timeout: int = 10) -> bool:
        """DÜZELTME: Modal'ın hazır olmasını bekle - Gelişmiş"""
        print(f"🔍 Modal hazır mı kontrol ediliyor... (timeout: {timeout}s)")

        start_time = time.time()
        attempt = 0
        last_error = None

        while time.time() - start_time < timeout:
            attempt += 1

            try:
                # DÜZELTME: Adım adım detaylı kontrol
                if not self.gui:
                    last_error = "GUI yok"
                    time.sleep(0.2)
                    continue

                if not hasattr(self.gui, 'data_entry_window'):
                    last_error = "data_entry_window attribute yok"
                    time.sleep(0.2)
                    continue

                if not self.gui.data_entry_window:
                    last_error = "data_entry_window None"
                    time.sleep(0.2)
                    continue

                # DÜZELTME: Widget varlık kontrolü
                try:
                    self.gui.data_entry_window.winfo_exists()
                except tk.TclError:
                    last_error = "data_entry_window widget mevcut değil"
                    time.sleep(0.2)
                    continue

                if not hasattr(self.gui, 'modal_entries'):
                    last_error = "modal_entries attribute yok"
                    time.sleep(0.2)
                    continue

                if not self.gui.modal_entries:
                    last_error = "modal_entries None"
                    time.sleep(0.2)
                    continue

                # DÜZELTME: Her entry widget'ını kontrol et
                entries_ok = True
                for key, entry in self.gui.modal_entries.items():
                    try:
                        entry.winfo_exists()
                    except (tk.TclError, AttributeError):
                        last_error = f"Entry widget {key} mevcut değil"
                        entries_ok = False
                        break

                if not entries_ok:
                    time.sleep(0.2)
                    continue

                # Tüm kontroller geçti!
                print(f"✅ Modal hazır! (deneme {attempt})")
                self.log_step("✅ Modal form hazır", 0.5)
                return True

            except Exception as e:
                last_error = f"Kontrol hatası: {e}"
                time.sleep(0.2)
                continue

        print(f"❌ Modal timeout! ({timeout}s) - Son hata: {last_error}")
        return False

    def find_modal_form(self):
        """DÜZELTME: Modal formu güvenli şekilde bul"""
        if not self.gui:
            return None

        try:
            # DÜZELTME: Adım adım güvenli kontrol
            if not hasattr(self.gui, 'data_entry_window') or not self.gui.data_entry_window:
                return None

            # Widget varlığını kontrol et
            self.gui.data_entry_window.winfo_exists()

            if not hasattr(self.gui, 'modal_entries') or not self.gui.modal_entries:
                return None

            # Her entry'yi kontrol et
            for key, entry in self.gui.modal_entries.items():
                try:
                    entry.winfo_exists()
                except (tk.TclError, AttributeError):
                    self.log_step(f"⚠️ Entry {key} mevcut değil", 0.1)
                    return None

            return self.gui.modal_entries

        except tk.TclError:
            self.log_step("⚠️ Modal form kontrol hatası", 0.1)
            return None
        except Exception as e:
            self.log_step(f"⚠️ Modal form bulma hatası: {e}", 0.1)
            return None

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
        """DÜZELTME: Notebook widget access"""
        if not self.gui or not hasattr(self.gui, "notebook"):
            return None
        try:
            # Widget'ın varlığını kontrol et
            self.gui.notebook.winfo_exists()

            # Index geçerli mi kontrol et
            if index >= len(self.gui.notebook.tabs()):
                return None

            # Güvenli erişim
            tab_id = self.gui.notebook.tabs()[index]
            bbox = self.gui.notebook.bbox(tab_id)

            if bbox:
                x, y, w, h = bbox
                rootx = self.gui.notebook.winfo_rootx() + x
                rooty = self.gui.notebook.winfo_rooty() + y
                return self._BBoxWidget(rootx, rooty, w, h)
        except Exception as e:
            print(f"❌ Tab widget error: {e}")
            return None
        
    def move_mouse_to_widget(self, widget, smooth: bool = True):
        """DÜZELTME: Fareyi widget'a yumuşak hareketle taşı - Gelişmiş hata yönetimi"""
        if not self.mouse_simulation:
            return

        try:
            self.focus_window()

            # DÜZELTME: Widget koordinat kontrolü
            try:
                x = widget.winfo_rootx() + widget.winfo_width() // 2
                y = widget.winfo_rooty() + widget.winfo_height() // 2
            except (tk.TclError, AttributeError) as e:
                self.log_step(f"⚠️ Widget koordinat hatası: {e}", 0.1)
                return

            # DÜZELTME: Ekran sınırları kontrolü
            screen_width, screen_height = pyautogui.size()
            if not (0 <= x <= screen_width and 0 <= y <= screen_height):
                self.log_step(f"⚠️ Koordinat ekran dışında: ({x}, {y})", 0.1)
                return

            # Küçük rastgele offset (daha doğal)
            x += random.randint(-5, 5)
            y += random.randint(-2, 2)

            # DÜZELTME: Sınırları tekrar kontrol et
            x = max(0, min(x, screen_width - 1))
            y = max(0, min(y, screen_height - 1))

            # Yumuşak hareket - hata yönetimi ile
            duration = 0.3 if smooth else 0.1
            try:
                pyautogui.moveTo(x, y, duration=duration)
            except pyautogui.FailSafeException:
                self.log_step("⚠️ PyAutoGUI FailSafe tetiklendi", 0.1)
                return
            except Exception as e:
                self.log_step(f"⚠️ Mouse hareket hatası: {e}", 0.1)
                return

            # Çok kısa bekleme (gerçekçi)
            time.sleep(random.uniform(0.05, 0.15) * self.delay_factor)

        except Exception as e:
            self.log_step(f"⚠️ Mouse hareket genel hatası: {e}", 0.1)
            
    def click_widget_simulation(
        self, widget_name: str, widget=None, delay: float = 0.5, call_after: bool = True
    ):
        """DÜZELTME: Widget tıklama simülasyonu - Gelişmiş hata yönetimi"""
        self.log_step(f"🖱️ {widget_name} tıklanıyor...", 0.2)

        if widget and self.mouse_simulation:
            try:
                widget.winfo_exists()
            except (tk.TclError, AttributeError):
                self.log_step(f"⚠️ Widget {widget_name} mevcut değil", 0.1)
                return

            try:
                self.call_in_gui_thread(self.move_mouse_to_widget, widget, True)
                self.call_in_gui_thread(self.highlight_widget, widget)
            except Exception as e:
                self.log_step(f"⚠️ Mouse/highlight hatası: {e}", 0.1)

        time.sleep(random.uniform(0.1, 0.3) * self.delay_factor)
        self.log_step(f"✅ {widget_name} başarıyla tıklandı", delay)

        if call_after:
            try:
                self.call_in_gui_thread(self.after_mouse_click)
            except Exception as e:
                self.log_step(f"⚠️ After mouse click hatası: {e}", 0.1)

    def _find_save_button(self):
        """DÜZELTME: Save butonunu güvenli şekilde bul"""
        if not self.gui or not hasattr(self.gui, 'data_entry_window'):
            return None
        try:
            for widget in self.gui.data_entry_window.winfo_children():
                if hasattr(widget, 'winfo_children'):
                    for child in widget.winfo_children():
                        if hasattr(child, 'cget'):
                            try:
                                text_val = child.cget('text')
                            except tk.TclError:
                                continue
                            if 'Kaydet' in str(text_val):
                                return child
        except Exception:
            return None
        return None
        
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
        self.click_widget_simulation("Dashboard sekmesi", dashboard_widget, call_after=False)
        self.call_in_gui_thread(self.gui.notebook.select, 0)

        # Düzensiz bir rota için 4 farklı sekmeyi rastgele seç
        available_indices = list(tab_keys.keys())
        if 0 in available_indices:
            available_indices.remove(0)

        random_tabs = random.sample(available_indices, 4)

        for idx in random_tabs:
            name = tab_keys.get(idx, f"Tab {idx}")
            widget = self.get_tab_widget(idx)
            self.click_widget_simulation(f"{name} sekmesi", widget, call_after=False)
            self.call_in_gui_thread(self.gui.notebook.select, idx)

        # En son Dashboard sekmesine geri dön
        self.log_step("↩️ Dashboard sekmesine dönülüyor...", 0.5)
        self.click_widget_simulation("Dashboard sekmesi", dashboard_widget, call_after=False)
        self.call_in_gui_thread(self.gui.notebook.select, 0)

        self.log_step("✅ FAZ 1 TAMAMLANDI: Navigasyon tamamlandı", 1.0)
        
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
            cont = step_function()
            if cont is False:
                self.log_step(f"⏹️ {step_name} kullanıcı tarafından iptal edildi", 0.5)
                return
            self.log_step(f"✅ {step_name} tamamlandı", 0.8)
            
        self.log_step("✅ FAZ 2 TAMAMLANDI: 6 adımlı süreç bitti", 1.5)
        
    def execute_step1_source_selection(self):
        """Adım 1: USER INPUT BEKLE"""
        print("🔵 Adım 1 başlıyor...")

        user_confirmed = self.call_in_gui_thread(self.gui.step1_select_source)

        timeout = 60
        start_time = time.time()

        while time.time() - start_time < timeout:
            time.sleep(0.5)
            if not self._is_popup_open():
                break

        print("✅ Adım 1 USER TARAFINDAN tamamlandı")
        return bool(user_confirmed)
        
    def execute_step2_record_filtering(self):
        """Adım 2: YES/NO BEKLE"""
        print("🔵 Adım 2 başlıyor...")

        result = self.call_in_gui_thread(self.gui.step2_filter_records)

        timeout = 60
        start_time = time.time()

        while time.time() - start_time < timeout:
            time.sleep(0.5)
            if not self._is_popup_open():
                break

        print("✅ Adım 2 USER TARAFINDAN tamamlandı")
        return bool(result)
        
    def execute_step3_data_preview(self):
        """Adım 3: Veri önizleme - TEMİZ"""
        print("🔵 Adım 3 başlıyor...")

        # Önizleme için ilk Excel dosyasındaki kayıtları hazırla
        preview_records = self.prepare_preview_records()

        if self.gui:
            self.call_in_gui_thread(self.gui.set_current_records, preview_records)

        self.call_in_gui_thread(self.gui.step3_preview_data)
        print("✅ Adım 3 tamamlandı")
        return True

    def prepare_preview_records(self) -> List[Dict]:
        """İlk Excel dosyasından kayıtları önizleme için hazırla"""
        if not self.excel_files:
            self.log_step("⚠️ Önizleme için Excel dosyası bulunamadı", 0.5)
            return []

        excel_path = self.excel_files[0]
        try:
            self.log_step(f"📂 Önizleme dosyası okunuyor: {excel_path.name}", 0.5)
            raw_data = pd.read_excel(excel_path, header=23)
            pattern = r'^POSH.*\/\d{15}$'
            aciklama_cols = [col for col in raw_data.columns if 'açıklama' in str(col).lower()]
            aciklama_col = aciklama_cols[0] if aciklama_cols else raw_data.columns[2]

            filtered_data = raw_data[raw_data[aciklama_col].astype(str).str.match(pattern, na=False)]

            processed_records = []
            for _, row in filtered_data.iterrows():
                record = {
                    'tarih': str(row.iloc[0]) if len(row) > 0 else datetime.now().strftime('%d.%m.%Y'),
                    'aciklama': str(row[aciklama_col]) if pd.notna(row[aciklama_col]) else "",
                    'tutar': str(row.iloc[3]) if len(row) > 3 else "0",
                    'dosya': excel_path.name
                }
                processed_records.append(record)

            self.log_step(f"🔍 Önizleme için {len(processed_records)} kayıt hazırlandı", 0.5)
            return processed_records

        except Exception as e:
            self.log_step(f"❌ Önizleme hazırlama hatası: {e}", 0.5)
            return []
        
    def execute_step4_parameters(self):
        """Adım 4: İşlem parametreleri - TEMİZ"""
        print("🔵 Adım 4 başlıyor...")
        self.call_in_gui_thread(self.gui.step4_set_parameters)
        print("✅ Adım 4 tamamlandı")
        return True
        
    def execute_step5_data_entry(self):
        """Adım 5: MODAL AÇILMASINI BEKLE"""
        self.log_step("🚀 Adım 5: Modal açılıyor...", 1.0)

        self.call_in_gui_thread(self.gui.step5_start_data_entry)

        timeout = 120
        start_time = time.time()

        while time.time() - start_time < timeout:
            time.sleep(1)
            if self.wait_for_modal_ready(5):
                self.log_step("✅ Modal açıldı", 0.5)
                break

        while time.time() - start_time < timeout:
            time.sleep(1)
            if not self._is_popup_open():
                self.log_step("✅ User onayladı", 0.5)
                break

        # Adım 5 sonunda modal açık bırakılır
        return True
        
    def execute_step6_batch_confirm(self):
        """Adım 6: Toplu onay - TEMİZ"""
        print("🔵 Adım 6 başlıyor...")
        self.call_in_gui_thread(self.gui.step6_batch_confirm)
        print("✅ Adım 6 tamamlandı")
        return True
        
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
        """DÜZELTME: Tek kayıt işleme - Gelişmiş hata yönetimi"""
        try:
            if not self.wait_for_modal_ready(5):
                self.log_step("⚠️ Modal form hazır değil, kayıt atlanıyor", 0.5)
                return False

            modal_entries = self.find_modal_form()
            if not modal_entries:
                self.log_step("⚠️ Modal form bulunamadı, kayıt atlanıyor", 0.5)
                return False

            entries = modal_entries

            field_operations = [
                ('date_entry', record['tarih'], "📅 Tarih"),
                ('desc_entry', record['aciklama'][:80] + "..." if len(record['aciklama']) > 80 else record['aciklama'], "📝 Açıklama"),
                ('amount_entry', record['tutar'], "💰 Tutar"),
                ('file_entry', record['dosya'], "📁 Dosya")
            ]

            for field_key, field_value, field_desc in field_operations:
                try:
                    if field_key not in entries:
                        self.log_step(f"⚠️ {field_key} alanı bulunamadı", 0.2)
                        continue

                    self.log_step(f"{field_desc} giriliyor: {str(field_value)[:30]}...", 0.3)
                    try:
                        entries[field_key].winfo_exists()
                    except tk.TclError:
                        self.log_step(f"⚠️ {field_key} widget'ı mevcut değil", 0.2)
                        continue

                    self.click_widget_simulation(f"{field_desc} alanı", entries.get(field_key), delay=0.3)
                    result = self.call_in_gui_thread(self.fill_entry_field, entries[field_key], str(field_value))
                    if result is None:
                        self.log_step(f"⚠️ {field_key} doldurma başarısız", 0.2)

                except Exception as e:
                    self.log_step(f"⚠️ {field_key} işleme hatası: {e}", 0.2)
                    continue

            self.log_step("💾 Kayıt kaydediliyor...", 0.5)

            try:
                save_button = self._find_save_button()
                if save_button:
                    self.click_widget_simulation("Kaydet butonu", save_button, delay=0.5)

                result = self.call_in_gui_thread(self.gui.save_advanced_record)
                if result is None:
                    self.log_step("⚠️ Kaydetme işlemi başarısız", 0.3)
                    return False

            except Exception as e:
                self.log_step(f"⚠️ Kaydetme hatası: {e}", 0.3)
                return False

            self.log_step(f"✅ Kayıt {record_num}/{total} başarıyla işlendi", 0.8)
            return True

        except Exception as e:
            self.log_step(f"❌ Kayıt işleme genel hatası: {e}", 0.5)
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
        """4. Faz: SADECE TÜM İŞLEMLER BİTTİKTEN SONRA"""
        self.log_step("🎯 FAZ 4: GERÇEKTEN sonlandırma...", 1.0)

        if not self.excel_files or len(self.results) == 0:
            self.log_step("⚠️ Henüz hiç Excel işlenmedi - FAZ 4 erken!", 1.0)
            return

        processed_files = len([r for r in self.results if r.get('success', 0) > 0])
        if processed_files == 0:
            self.log_step("⚠️ Hiç dosya başarıyla işlenmedi - FAZ 4 erken!", 1.0)
            return

        self.log_step("✅ Gerçekten tüm işlemler bitti - FAZ 4 başlıyor", 1.0)

        self.log_step("✅ Adım 6: Toplu onay işlemi gerçekleştiriliyor...", 1.0)
        self.call_in_gui_thread(self.gui.step6_batch_confirm)

        total_files = len(self.excel_files)
        total_records = self.total_records_processed
        success_rate = (
            total_records / (total_records + self.failed_records) * 100
        ) if (total_records + self.failed_records) > 0 else 0
        processing_time = time.time() - self.start_time if self.start_time else 0

        self.log_step("📊 SONUÇ RAPORU:", 1.0)
        self.log_step(f"   📁 İşlenen Dosya Sayısı: {total_files}", 0.3)
        self.log_step(f"   📋 Toplam Kayıt Sayısı: {total_records}", 0.3)
        self.log_step(f"   ✅ Başarılı İşlemler: {total_records}", 0.3)
        self.log_step(f"   ❌ Başarısız İşlemler: {self.failed_records}", 0.3)
        self.log_step(f"   📈 Başarı Oranı: %{success_rate:.1f}", 0.3)
        self.log_step(f"   ⏱️ Toplam Süre: {processing_time:.1f} saniye", 0.3)

        self.show_final_completion_dialog(total_records, total_files, success_rate)

        # Opsiyonel: Modal hâlâ açıksa kapat
        if self.gui and getattr(self.gui, 'data_entry_window', None):
            self.call_in_gui_thread(self.gui.close_modal)

        self.log_step("✅ FAZ 4 TAMAMLANDI: Tüm işlemler bitti", 2.0)

    def show_final_completion_dialog(self, total_records: int, total_files: int, success_rate: float):
        """Final tamamlanma dialog'u"""
        if not self.gui:
            return

        def show_dialog():
            completion_dialog = tk.Toplevel(self.gui.root)
            completion_dialog.title("🎉 RPA İşlemi Tamamlandı")
            completion_dialog.geometry("500x350")
            completion_dialog.configure(bg='#1e1e2e')

            # Merkezi konum
            x = (completion_dialog.winfo_screenwidth() // 2) - 250
            y = (completion_dialog.winfo_screenheight() // 2) - 175
            completion_dialog.geometry(f"500x350+{x}+{y}")

            # Üstte kal ve modal yap
            completion_dialog.attributes('-topmost', True)
            completion_dialog.grab_set()
            completion_dialog.focus_set()

            tk.Label(completion_dialog, text="🎉", font=('Segoe UI', 48), bg='#1e1e2e', fg='#a6e3a1').pack(pady=20)
            tk.Label(
                completion_dialog,
                text="RPA İşlemi Başarıyla Tamamlandı!",
                font=('Segoe UI', 16, 'bold'),
                bg='#1e1e2e',
                fg='#cdd6f4',
            ).pack(pady=10)

            stats_text = f"""
📊 İşlem Sonuçları:
        
📁 İşlenen Dosya: {total_files}
📋 Toplam Kayıt: {total_records}
📈 Başarı Oranı: %{success_rate:.1f}
⏱️ Süre: {time.time() - self.start_time:.1f} saniye

✅ Tüm veriler sisteme aktarıldı!
        """

            tk.Label(
                completion_dialog,
                text=stats_text,
                font=('Segoe UI', 11),
                justify='center',
                bg='#1e1e2e',
                fg='#cdd6f4',
            ).pack(pady=20)

            tk.Button(
                completion_dialog,
                text="Tamam",
                command=completion_dialog.destroy,
                bg='#89b4fa',
                fg='#1e1e2e',
                font=('Segoe UI', 12, 'bold'),
                width=15,
                height=2,
            ).pack(pady=20)

        self.call_in_gui_thread(show_dialog)
        
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
        """DÜZELTME: RPA'yi direkt çalıştır - thread yok"""
        if not self.gui:
            self.log_step("❌ GUI referansı ayarlanmamış!", 1.0)
            return None

        if excel_files:
            self.set_processing_files(excel_files)

        self.is_running = True
        self.progress_callback = progress_callback

        # DÜZELTME: Thread kullanma, direkt çalıştır
        try:
            print("🚀 RPA direkt başlatılıyor...")
            self.run_complete_automation_sequence()

            # Progress callback ile sonucu bildir
            if self.progress_callback:
                self.progress_callback(1.0, "Tüm dosyalar işlendi")

            return self.get_results()

        except Exception as e:
            self.log_step(f"❌ RPA Hatası: {e}", 1.0)
            return []
        finally:
            self.is_running = False
        
    def get_results(self) -> List[Dict[str, Any]]:
        """İşlem sonuçlarını döndür"""
        return self.results
        
    def stop(self):
        """RPA'yi durdur"""
        self.is_running = False
        print("🛑 RPA sistemi durduruldu")

# Test fonksiyonu
if __name__ == "__main__":
    print("🤖 Karmaşık RPA Motoru - Test Modu")
    bot = EnterpriseRPABot()
    bot.set_processing_speed("fast")
    print("✅ RPA motoru hazır")
