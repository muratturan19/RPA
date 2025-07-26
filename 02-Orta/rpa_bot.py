import time
import threading
import pandas as pd
from pathlib import Path


class AdvancedRPABot:
    """Otomasyon adimlarini yurutmek icin gelismis RPA botu."""

    def __init__(self):
        self.gui = None
        self.is_running = False
        self.current_step = ""

    def set_gui_reference(self, gui_app):
        """GUI referansini ayarla"""
        self.gui = gui_app
        print("✅ GUI referansı ayarlandı")

    def log_step(self, message):
        """Her adimi logla ve GUI uzerinden durumu guncelle"""
        self.current_step = message
        print(f"[RPA] {message}")
        if self.gui:
            self.gui.update_status(f"RPA: {message}")

    def load_test_excel(self):
        """Test Excel dosyasini veya ornek veriyi yukle"""
        self.log_step("Test Excel verisi yükleniyor...")

        # 🔧 DEBUG: Excel yol kontrolü
        excel_path = Path("../data/Vadesiz_Hesap_Detay.xlsx")
        print(f"DEBUG: Excel path 1: {excel_path} - Exists: {excel_path.exists()}")

        if not excel_path.exists():
            excel_path = Path("data/Vadesiz_Hesap_Detay.xlsx")
            print(f"DEBUG: Excel path 2: {excel_path} - Exists: {excel_path.exists()}")

        if excel_path.exists():
            # 🔧 DEBUG: Excel okuma
            raw_data = pd.read_excel(excel_path)
            print(f"DEBUG: Raw Excel shape: {raw_data.shape}")
            print(f"DEBUG: Raw columns: {list(raw_data.columns)}")
            print(f"DEBUG: First 3 rows:\n{raw_data.head(3)}")

            # 🔧 DEBUG: GUI'ye veri atama
            self.gui.data = raw_data
            print(f"DEBUG: GUI data assigned: {len(self.gui.data)} rows")

            # 🔧 DEBUG: show_data çağrısı
            print("DEBUG: Calling gui.show_data()...")
            self.gui.show_data(self.gui.data)
            print("DEBUG: show_data() completed")

            # 🔧 DEBUG: Treeview kontrol
            tree_children = self.gui.tree.get_children()
            print(f"DEBUG: Tree children count: {len(tree_children)}")

            self.gui.update_summary()
            self.log_step(f"✅ Excel yüklendi: {len(self.gui.data)} kayıt")
            return True
        else:
            print("DEBUG: Excel not found, creating test data...")
            try:
                self.create_test_data()
                return True
            except Exception as e:
                self.log_step(f"❌ Excel yükleme hatası: {e}")
                return False

    def create_test_data(self):
        """Excel bulunamazsa ornek veri olustur"""
        self.log_step("Test verisi oluşturuluyor...")
        test_data = pd.DataFrame([
            {
                "Tarih": "23.07.2025",
                "Açıklama": "POSH/20250723/000000002391280/N042 K P POS Satış /000001660659421",
                "Tutar": 670.99,
            },
            {
                "Tarih": "23.07.2025",
                "Açıklama": "POSH/20250723/000000002391280/N042 K P ÜİY Komisyon /000001660659421",
                "Tutar": -13.42,
            },
            {
                "Tarih": "23.07.2025",
                "Açıklama": "POSH/20250723/000000002391280/TY01 N P POS Satış /000001660659422",
                "Tutar": 307.49,
            },
            {
                "Tarih": "23.07.2025",
                "Açıklama": "POSH/20250723/000000002391280/TY01 N P ÜİY Komisyon /000001660659422",
                "Tutar": -8.46,
            },
            {
                "Tarih": "23.07.2025",
                "Açıklama": "POSH/20250723/000000002391280 MUSLUOĞLU BAKLAVA4",
                "Tutar": -41563.5,
            },
            {
                "Tarih": "24.07.2025",
                "Açıklama": "POSH/20250724/000000002391280/N001 N P POS Satış /000001661601485",
                "Tutar": 4559.47,
            },
        ])
        self.gui.data = test_data
        self.gui.show_data(test_data)
        self.gui.update_summary()
        self.log_step(f"✅ Test verisi oluşturuldu: {len(test_data)} kayıt")

    def set_pattern_filter(self, pattern):
        """Desen filtresini ayarla"""
        self.log_step(f"Pattern ayarlanıyor: {pattern}")
        self.gui.pattern_var.set(pattern)
        time.sleep(1.5)
        self.log_step("✅ Pattern ayarlandı")

    def set_amount_filters(self, min_amount=None, max_amount=None):
        """Tutar filtrelerini ayarla"""
        if min_amount is not None:
            self.log_step(f"Min tutar ayarlanıyor: {min_amount}")
            self.gui.min_amount.delete(0, "end")
            self.gui.min_amount.insert(0, str(min_amount))
            time.sleep(0.9)
        if max_amount is not None:
            self.log_step(f"Max tutar ayarlanıyor: {max_amount}")
            self.gui.max_amount.delete(0, "end")
            self.gui.max_amount.insert(0, str(max_amount))
            time.sleep(0.9)

    def select_account(self, account):
        """Hesap secimi yap"""
        self.log_step(f"Hesap seçiliyor: {account}")
        self.gui.account_combo.set(account)
        time.sleep(1.5)
        self.log_step("✅ Hesap seçildi")

    def apply_filters(self):
        """Filtreleri uygula"""
        self.log_step("Filtreler uygulanıyor...")
        try:
            self.gui.apply_advanced_filter()
            time.sleep(3)
            if hasattr(self.gui, "filtered_data") and not self.gui.filtered_data.empty:
                filtered_count = len(self.gui.filtered_data)
            else:
                filtered_count = 0
            self.log_step(f"✅ Filtre uygulandı: {filtered_count} kayıt bulundu")
            return filtered_count
        except Exception as e:
            self.log_step(f"❌ Filtre hatası: {e}")
            return 0

    def clear_all_filters(self):
        """Tum filtreleri temizle"""
        self.log_step("Filtreler temizleniyor...")
        self.gui.clear_filters()
        time.sleep(1.5)
        self.log_step("✅ Filtreler temizlendi")

    def analyze_results(self):
        """Filtrelenmis verileri analiz et"""
        self.log_step("Sonuçlar analiz ediliyor...")
        if hasattr(self.gui, "filtered_data") and not self.gui.filtered_data.empty:
            data = self.gui.filtered_data
        else:
            data = self.gui.data
        if data.empty:
            self.log_step("❌ Analiz edilecek veri yok")
            return
        total_records = len(data)
        if "Tutar" in data.columns:
            positive_sum = data[data["Tutar"] > 0]["Tutar"].sum()
            negative_sum = data[data["Tutar"] < 0]["Tutar"].sum()
            net_balance = data["Tutar"].sum()
            self.log_step(f"📊 Analiz: {total_records} kayıt")
            self.log_step(f"💰 Pozitif: {positive_sum:,.2f} TL")
            self.log_step(f"💸 Negatif: {negative_sum:,.2f} TL")
            self.log_step(f"📈 Net: {net_balance:,.2f} TL")
        if "Açıklama" in data.columns:
            pos_count = len(data[data["Açıklama"].str.contains("POS Satış", na=False)])
            komisyon_count = len(data[data["Açıklama"].str.contains("ÜİY Komisyon", na=False)])
            musluoglu_count = len(data[data["Açıklama"].str.contains("MUSLUOĞLU", na=False)])
            self.log_step(f"🏪 POS Satış: {pos_count} adet")
            self.log_step(f"💸 ÜİY Komisyon: {komisyon_count} adet")
            self.log_step(f"🚫 MUSLUOĞLU (hariç): {musluoglu_count} adet")

    def run_automation_sequence(self):
        """Tum otomasyon adimlarini calistir"""
        self.log_step("🤖 RPA Otomasyonu başlatılıyor...")
        if not self.load_test_excel():
            return
        time.sleep(3)
        self.log_step("--- TEST 1: Doğru POSH Pattern ---")
        self.set_pattern_filter(r"^POSH.*\/\d{15}$")
        result1 = self.apply_filters()
        self.analyze_results()
        time.sleep(6)
        self.log_step("--- TEST 2: MUSLUOĞLU Hariç Pattern ---")
        self.clear_all_filters()
        self.set_pattern_filter(r"^POSH(?!.*MUSLUOĞLU).*\/\d{15}$")
        result2 = self.apply_filters()
        self.analyze_results()
        time.sleep(6)
        self.log_step("--- TEST 3: Tutar Filtreleri ---")
        self.clear_all_filters()
        self.set_pattern_filter(r"^POSH.*\/\d{15}$")
        self.set_amount_filters(min_amount=100, max_amount=5000)
        result3 = self.apply_filters()
        self.analyze_results()
        time.sleep(6)
        self.log_step("--- TEST 4: Hesap Seçimi ---")
        self.select_account("6232011 - GARANTİ BANKASI")
        time.sleep(3)
        self.log_step("🎉 RPA Otomasyonu tamamlandı!")
        self.log_step(f"📊 Test sonuçları: {result1}/{result2}/{result3} kayıt")

    def run(self):
        """RPA'yi thread uzerinde calistir"""
        if not self.gui:
            print("❌ GUI referansı ayarlanmamış!")
            return
        self.is_running = True

        def automation_worker():
            try:
                self.run_automation_sequence()
            except Exception as e:
                self.log_step(f"❌ RPA Hatası: {e}")
            finally:
                self.is_running = False

        thread = threading.Thread(target=automation_worker, daemon=True)
        thread.start()
        return thread

