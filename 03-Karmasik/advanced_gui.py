"""
Karmaşık GUI Sistemi - Enterprise RPA için 6-7 Adımlı Navigasyon
Gerçekçi ERP/Muhasebe programı simülasyonu
"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pandas as pd
from datetime import datetime
import time

class EnterpriseGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("\U0001f3e2 Enterprise ERP Sistemi - Karmaşık RPA Demo")
        self.root.geometry("1600x900")
        self.root.state('zoomed')
        
        # Veri depolama
        self.main_data = []
        self.current_records = []
        self.processing_files = []
        
        # Modal referansları
        self.data_entry_window = None
        self.confirmation_dialog = None
        
        # GUI'yi öne getir
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        
        self.setup_enterprise_styles()
        self.create_enterprise_interface()
        
    def setup_enterprise_styles(self):
        """Enterprise seviye görsel stil"""
        style = ttk.Style()
        style.theme_use('clam')

        # Koyu enterprise tema
        style.configure('Enterprise.TNotebook', 
                       tabposition='n', 
                       background='#1e1e2e')
        style.configure('Enterprise.TNotebook.Tab',
                       padding=[20, 12],
                       background='#313244',
                       foreground='#cdd6f4',
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        style.map('Enterprise.TNotebook.Tab',
                  background=[('selected', '#89b4fa')],
                  foreground=[('selected', '#1e1e2e')])

        # Toolbar temaları
        style.configure('MainToolbar.TFrame',
                       background='#181825',
                       relief='flat')
        style.configure('SubToolbar.TFrame',
                       background='#313244',
                       relief='flat')

        # Buton temaları
        style.configure('Primary.TButton',
                       background='#89b4fa',
                       foreground='#1e1e2e',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 9, 'bold'))
        style.map('Primary.TButton',
                  background=[('active', '#74c0fc')])
                  
        style.configure('Secondary.TButton',
                       background='#f38ba8',
                       foreground='#1e1e2e',
                       borderwidth=0,
                       focuscolor='none')
        style.map('Secondary.TButton',
                  background=[('active', '#eba0ac')])
                  
        style.configure('Success.TButton',
                       background='#a6e3a1',
                       foreground='#1e1e2e',
                       borderwidth=0,
                       focuscolor='none')
        
        # Card stil
        style.configure('Card.TLabelframe',
                       background='#313244',
                       foreground='#cdd6f4',
                       borderwidth=2,
                       relief='solid')
        style.configure('Card.TLabelframe.Label',
                       background='#313244',
                       foreground='#89b4fa',
                       font=('Segoe UI', 11, 'bold'))
        
    def create_enterprise_interface(self):
        """Enterprise seviye arayüz"""
        # Ana menü sistemi
        self.create_comprehensive_menu()
        
        # Ana toolbar
        self.create_main_toolbar()
        
        # Sekme sistemi (6 ana modül)
        self.create_module_tabs()
        
        # Ana içerik alanları
        self.create_module_contents()
        
        # Alt status bar
        self.create_enterprise_status_bar()
        
    def create_comprehensive_menu(self):
        """Kapsamlı menü sistemi"""
        menubar = tk.Menu(self.root, background='#181825', foreground='#cdd6f4')
        self.root.config(menu=menubar)
        
        # Ana modüller
        modules = {
            "\U0001f3e0 Ana Sayfa": ["Dashboard", "Hızlı Erişim", "Raporlar", "Ayarlar"],
            "\U0001f4bc Muhasebe": ["Hesap Planı", "Yevmiye", "Mizan", "Bilanço", "Gelir Tablosu"],
            "\U0001f4b0 Finans": ["Nakit Akışı", "Banka", "Kasa", "Çek-Senet", "Kredi Kartı"],
            "\U0001f4ca Finans-Tahsilat": ["Tahsilat İşlemleri", "Müşteri Hesapları", "Vadeli İşlemler", "Komisyon"],
            "\U0001f6d2 Satış": ["Sipariş", "Fatura", "İade", "Müşteri", "Fiyat Listesi"],
            "\U0001f4e6 Stok": ["Stok Kartları", "Giriş-Çıkış", "Sayım", "Transfer", "Depo"],
            "\U0001f465 Personel": ["Bordro", "Puantaj", "İzin", "Mesai", "SGK"],
            "\U0001f3ed Üretim": ["Üretim Emri", "Malzeme İhtiyacı", "Kapasite", "Kalite"],
            "\U0001f4c8 Raporlar": ["Mali Tablolar", "Analitik", "Grafik", "Dashboard"],
            "\u2699\ufe0f Sistem": ["Kullanıcılar", "Yetki", "Backup", "Log", "Parametreler"]
        }
        
        for module_name, sub_menus in modules.items():
            module_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label=module_name, menu=module_menu)
            
            for sub_menu in sub_menus:
                module_menu.add_command(
                    label=sub_menu,
                    command=lambda m=module_name, s=sub_menu: self.menu_selected(m, s)
                )
                
    def create_main_toolbar(self):
        """Ana toolbar"""
        toolbar_frame = ttk.Frame(self.root, style='MainToolbar.TFrame', height=60)
        toolbar_frame.pack(fill='x')
        toolbar_frame.pack_propagate(False)
        
        # Sol taraf - hızlı erişim
        left_frame = ttk.Frame(toolbar_frame, style='MainToolbar.TFrame')
        left_frame.pack(side='left', fill='y', padx=10)
        
        quick_buttons = [
            ("\U0001f3e0", "Ana Sayfa", self.go_home),
            ("\U0001f4ca", "Dashboard", self.open_dashboard),
            ("\U0001f4be", "Kaydet", self.quick_save),
            ("\U0001f50d", "Ara", self.quick_search),
            ("\U0001f5a8\ufe0f", "Yazdır", self.quick_print)
        ]
        
        for icon, tooltip, command in quick_buttons:
            btn = ttk.Button(left_frame, text=icon, command=command, width=4)
            btn.pack(side='left', padx=2, pady=10)
            
        # Orta - başlık
        title_label = ttk.Label(toolbar_frame, 
                               text="\U0001f3e2 Enterprise ERP Sistemi v5.0", 
                               font=('Segoe UI', 14, 'bold'),
                               background='#181825',
                               foreground='#89b4fa')
        title_label.pack(side='left', expand=True, padx=20)
        
        # Sağ taraf - kullanıcı bilgisi
        user_frame = ttk.Frame(toolbar_frame, style='MainToolbar.TFrame')
        user_frame.pack(side='right', fill='y', padx=10)
        
        ttk.Label(user_frame, 
                 text=f"\U0001f464 Admin | {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                 background='#181825',
                 foreground='#cdd6f4').pack(side='right', pady=15)
        
    def create_module_tabs(self):
        """Ana modül sekmeleri"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        self.notebook = ttk.Notebook(main_frame, style='Enterprise.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # 6 ana modül sekmesi
        self.tabs = {}
        tab_configs = [
            ("\U0001f4ca Dashboard", "dashboard"),
            ("\U0001f4bc Muhasebe", "accounting"),
            ("\U0001f4b0 Finans-Tahsilat", "finance"),  # ANA SEKME
            ("\U0001f4e6 Stok", "inventory"),
            ("\U0001f4c8 Raporlar", "reports"),
            ("\u2699\ufe0f Sistem", "system")
        ]
        
        for tab_name, tab_key in tab_configs:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=tab_name)
            self.tabs[tab_key] = frame
            
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_changed)
        
    def create_module_contents(self):
        """Her modülün içeriğini oluştur"""
        # Dashboard modülü
        self.create_dashboard_module()
        
        # Finans-Tahsilat modülü (ANA MODÜL)
        self.create_finance_module()
        
        # Diğer modüller (basit içerik)
        for module in ["accounting", "inventory", "reports", "system"]:
            self.create_simple_module(module)
            
    def create_dashboard_module(self):
        """Dashboard modülü"""
        frame = self.tabs["dashboard"]
        
        # Başlık
        title_frame = ttk.Frame(frame)
        title_frame.pack(fill='x', pady=15, padx=20)
        
        ttk.Label(title_frame, 
                 text="\U0001f4ca Enterprise Dashboard", 
                 font=('Segoe UI', 18, 'bold')).pack(side='left')
                 
        # İstatistik kartları
        stats_frame = ttk.Frame(frame)
        stats_frame.pack(fill='x', pady=20, padx=20)
        
        stats = [
            ("Toplam İşlem", "0", "#a6e3a1"),
            ("Bugünkü İşlem", "0", "#89b4fa"),
            ("Aktif Dosya", "0", "#f9e2af"),
            ("Başarı Oranı", "%0", "#f38ba8")
        ]
        
        for i, (title, value, color) in enumerate(stats):
            card = ttk.LabelFrame(stats_frame, text=title, 
                                 padding=20, style='Card.TLabelframe')
            card.pack(side='left', fill='both', expand=True, padx=10)
            
            value_label = ttk.Label(card, text=value, 
                                   font=('Segoe UI', 24, 'bold'))
            value_label.pack()
            
            if i == 0:
                self.total_transactions_label = value_label
            elif i == 1:
                self.today_transactions_label = value_label
                
        # Ana tablo
        self.create_main_data_table(frame)
        
    def create_finance_module(self):
        """Finans-Tahsilat modülü - KARMAŞIK NAVIGASYON"""
        frame = self.tabs["finance"]
        
        # Başlık
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill='x', pady=15, padx=20)
        
        ttk.Label(header_frame, 
                 text="\U0001f4b0 Finans - Tahsilat İşlemleri", 
                 font=('Segoe UI', 16, 'bold')).pack(side='left')
                 
        # Alt modül sekmesi (2. seviye)
        sub_notebook = ttk.Notebook(frame)
        sub_notebook.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Alt sekmeler
        sub_tabs = [
            ("\U0001f4b3 Tahsilat", "collections"),
            ("\U0001f3e6 Banka İşlemleri", "banking"),
            ("\U0001f4cb Veri İşlemleri", "data_ops"),  # ANA ALT SEKME
            ("\U0001f4ca Raporlar", "finance_reports")
        ]
        
        self.sub_tabs = {}
        for tab_name, tab_key in sub_tabs:
            sub_frame = ttk.Frame(sub_notebook)
            sub_notebook.add(sub_frame, text=tab_name)
            self.sub_tabs[tab_key] = sub_frame
            
        # Veri İşlemleri alt sekmesinin içeriği
        self.create_data_operations_content()
        
        # Diğer alt sekmeler için basit içerik
        for key in ["collections", "banking", "finance_reports"]:
            ttk.Label(self.sub_tabs[key], 
                     text=f"{key.title()} modülü henüz geliştirilmemiş.",
                     font=('Segoe UI', 12)).pack(pady=50)
                     
    def create_data_operations_content(self):
        """Veri İşlemleri içeriği - 6 ADIMLI SÜREÇ"""
        frame = self.sub_tabs["data_ops"]
        
        # Süreç adımları toolbar'ı
        process_frame = ttk.Frame(frame, style='SubToolbar.TFrame', height=80)
        process_frame.pack(fill='x', padx=10, pady=10)
        process_frame.pack_propagate(False)
        
        # Süreç adımları
        steps = [
            ("1\ufe0f\u20e3", "Hazırlık", "prepare"),
            ("2\ufe0f\u20e3", "Doğrulama", "validate"), 
            ("3\ufe0f\u20e3", "Veri Seçimi", "select_data"),
            ("4\ufe0f\u20e3", "İşlem Türü", "operation_type"),
            ("5\ufe0f\u20e3", "Veri Giriş", "data_entry"),  # ANA ADIM
            ("6\ufe0f\u20e3", "Onay & Kayıt", "confirm_save")
        ]
        
        for icon, name, key in steps:
            step_frame = ttk.Frame(process_frame)
            step_frame.pack(side='left', fill='both', expand=True, padx=5, pady=10)
            
            ttk.Label(step_frame, text=icon, 
                     font=('Segoe UI', 16)).pack()
            ttk.Label(step_frame, text=name, 
                     font=('Segoe UI', 9, 'bold')).pack()
                     
        # Ana işlem alanı
        operations_frame = ttk.LabelFrame(frame, text="\U0001f4cb Veri İşlem Merkezi", 
                                         padding=20, style='Card.TLabelframe')
        operations_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # İşlem butonları - KARMAŞIK HIYERARŞI
        button_rows = [
            # 1. Seviye butonları
            [
                ("\U0001f4c2 Veri Kaynağı Seç", self.step1_select_source, "Primary.TButton"),
                ("\U0001f50d Kayıt Filtrele", self.step2_filter_records, "Secondary.TButton"),
                ("\U0001f4ca Veri Önizleme", self.step3_preview_data, "Secondary.TButton")
            ],
            # 2. Seviye butonları  
            [
                ("\u2699\ufe0f İşlem Parametreleri", self.step4_set_parameters, "Secondary.TButton"),
                ("\U0001f4dd Veri Giriş Başlat", self.step5_start_data_entry, "Success.TButton"),  # ANA BUTON
                ("\u2705 Toplu Onay", self.step6_batch_confirm, "Primary.TButton")
            ]
        ]
        
        for i, button_row in enumerate(button_rows):
            row_frame = ttk.Frame(operations_frame)
            row_frame.pack(fill='x', pady=10)
            
            for text, command, style in button_row:
                btn = ttk.Button(row_frame, text=text, command=command, 
                               style=style, width=25)
                btn.pack(side='left', padx=10, pady=5)
                
        # Durum gösterimi
        self.process_status_label = ttk.Label(operations_frame,
                                            text="\U0001f7e1 Sistem hazır - Veri kaynağı seçin",
                                            font=('Segoe UI', 11, 'bold'))
        self.process_status_label.pack(pady=20)
        
    def create_simple_module(self, module_key):
        """Basit modül içeriği"""
        frame = self.tabs[module_key]
        ttk.Label(frame, 
                 text=f"{module_key.title()} modülü henüz geliştirilmemiş.",
                 font=('Segoe UI', 14)).pack(pady=100)
                 
    def create_main_data_table(self, parent):
        """Ana veri tablosu"""
        table_frame = ttk.LabelFrame(parent, text="\U0001f4cb İşlem Kayıtları", 
                                    padding=10, style='Card.TLabelframe')
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Treeview
        columns = ['ID', 'Tarih', 'Dosya', 'Açıklama', 'Tutar', 'Durum', 'Zaman']
        self.main_tree = ttk.Treeview(table_frame, columns=columns, 
                                     show='headings', height=12)
        
        widths = [50, 100, 150, 300, 120, 100, 120]
        for col, width in zip(columns, widths):
            self.main_tree.heading(col, text=col)
            self.main_tree.column(col, width=width, anchor='center' if col in ['ID', 'Tarih', 'Tutar', 'Durum', 'Zaman'] else 'w')
            
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', 
                                 command=self.main_tree.yview)
        self.main_tree.configure(yscrollcommand=scrollbar.set)
        
        self.main_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def create_enterprise_status_bar(self):
        """Alt durum çubuğu"""
        status_frame = ttk.Frame(self.root, style='MainToolbar.TFrame', height=30)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = ttk.Label(status_frame, 
                                     text="\U0001f7e2 Sistem Hazır - Enterprise ERP v5.0",
                                     background='#181825',
                                     foreground='#a6e3a1',
                                     font=('Segoe UI', 9))
        self.status_label.pack(side='left', padx=15, pady=5)
        
        # Sağ taraf bilgiler
        info_label = ttk.Label(status_frame,
                              text=f"\U0001f5a5\ufe0f Kullanıcı: Admin | \U0001f4c5 {datetime.now().strftime('%d.%m.%Y %H:%M:%S')} | \U0001f504 RPA Hazır",
                              background='#181825',
                              foreground='#cdd6f4',
                              font=('Segoe UI', 8))
        info_label.pack(side='right', padx=15, pady=5)
        
    # === ADIM FONKSİYONLARI ===
    
    def step1_select_source(self):
        """1. Adım: Veri kaynağı seç"""
        self.update_process_status("\U0001f535 1. Adım: Veri kaynağı belirleniyor...")
        self._show_info_left(
            "Adım 1",
            "Veri kaynağı seçimi tamamlandı.\n\n\U0001f4c2 Excel dosyaları hazırlandı."
        )
        self.update_process_status("\u2705 1. Adım tamamlandı - Filtreleme adımına geçin")
        
    def step2_filter_records(self):
        """2. Adım: Kayıt filtrele"""
        self.update_process_status("\U0001f535 2. Adım: Kayıtlar filtreleniyor...")
        result = self._ask_yes_no_left(
            "Adım 2",
            "POSH pattern filtresi uygulanacak.\n\nDevam edilsin mi?"
        )
        if result:
            self.update_process_status("\u2705 2. Adım tamamlandı - Önizleme yapın")
        else:
            self.update_process_status("\u26a0\ufe0f 2. Adım iptal edildi")
            
    def step3_preview_data(self):
        """3. Adım: Veri önizleme"""
        self.update_process_status("\U0001f535 3. Adım: Veri önizlemesi yapılıyor...")
        record_count = len(self.current_records) if self.current_records else 0
        self._show_info_left(
            "Adım 3",
            f"Veri önizlemesi:\n\n\U0001f4ca {record_count} kayıt bulundu\n\U0001f50d POSH pattern eşleşmesi\n\U0001f4b0 Tutar aralığı: dinamik"
        )
        self.update_process_status("\u2705 3. Adım tamamlandı - Parametreleri ayarlayın")
        
    def step4_set_parameters(self):
        """4. Adım: İşlem parametreleri"""
        self.update_process_status("\U0001f535 4. Adım: İşlem parametreleri ayarlanıyor...")
        params = simpledialog.askstring(
            "Adım 4",
            "İşlem parametrelerini girin\n(varsayılan: hızlı-mod)",
            initialvalue="hızlı-mod",
            parent=self.data_entry_window,
        )
        if params:
            self.update_process_status("\u2705 4. Adım tamamlandı - Veri girişi başlatabilirsiniz")
        else:
            self.update_process_status("\u26a0\ufe0f 4. Adım iptal edildi")
            

    def step5_start_data_entry(self):
        """5. Adım: VERİ GİRİŞ BAŞLAT - URGENT FIX"""
        print("🚀 step5_start_data_entry çağrıldı!")  # Debug log
        self.update_process_status("🚀 5. Adım: Veri giriş sistemi başlatılıyor...")

        # Onay dialog'u - BU KISMINDA SORUN VAR!
        record_count = len(self.current_records) if self.current_records else 0

        # URGENT: Dialog'u basitleştir, direkt modal aç
        print(f"📊 Kayıt sayısı: {record_count}")

        # URGENT: Onay dialog'unu geç, direkt modal aç
        self.update_process_status("✅ 5. Adım onaylandı - Veri Giriş Modal'ı açılıyor...")

        # URGENT: Hemen modal'ı aç - gecikme yok!
        try:
            print("🎯 Modal açılmaya çalışılıyor...")
            self.open_advanced_data_entry()
            print("✅ Modal açıldı!")

            # Modal açıldığını doğrula
            if self.data_entry_window and hasattr(self, 'modal_entries'):
                print("✅ Modal entries de mevcut!")
                self.update_process_status("✅ Modal hazır - RPA işleme başlayabilir")
            else:
                print("❌ Modal açıldı ama entries mevcut değil!")

        except Exception as e:
            print(f"❌ Modal açma hatası: {e}")
            self.update_process_status(f"❌ Modal açma hatası: {e}")

    def signal_modal_ready_to_rpa(self):
        """RPA'ya modal hazır sinyali gönder"""
        self.update_process_status("✅ Modal hazır - RPA işleme başlayabilir")
            
    def step6_batch_confirm(self):
        """6. Adım: Toplu onay"""
        self.update_process_status("\U0001f535 6. Adım: Toplu onay işlemi...")
        self._show_info_left("Adım 6", "Tüm kayıtlar onaylandı ve sisteme kaydedildi!")
        self.update_process_status("\U0001f389 6. Adım tamamlandı - İşlem süreci bitti!")
        
    def open_advanced_data_entry(self):
        """URGENT FIX: Gelişmiş Veri Giriş Modal'ı"""
        print("🚀 open_advanced_data_entry çağrıldı!")
        self.update_status("🚀 Gelişmiş Veri Giriş sistemi açılıyor...")

        # URGENT: Önceki modal'ı kapat
        if hasattr(self, 'data_entry_window') and self.data_entry_window:
            try:
                self.data_entry_window.destroy()
            except:
                pass
            self.data_entry_window = None

        # Modal pencere
        self.data_entry_window = tk.Toplevel(self.root)
        self.data_entry_window.title("🎯 Gelişmiş Veri Giriş Sistemi")

        # URGENT: Basit boyut ve konum
        self.data_entry_window.geometry("600x450+100+100")

        # URGENT: Basit modal ayarları
        self.data_entry_window.transient(self.root)
        self.data_entry_window.lift()
        self.data_entry_window.focus_set()

        print("🎯 Modal pencere oluşturuldu, içerik ekleniyor...")

        # Modal içeriği
        self.create_advanced_modal_content()

        print("✅ Modal içerik eklendi!")

        # URGENT: Modal'ın gerçekten hazır olduğunu doğrula
        self.root.update_idletasks()

        if hasattr(self, 'modal_entries') and self.modal_entries:
            print("✅ modal_entries hazır!")
            self.update_status("✅ Modal başarıyla açıldı ve hazır")
            return True
        else:
            print("❌ modal_entries hazır değil!")
            return False
        
    def create_advanced_modal_content(self):
        """Gelişmiş modal içeriği"""
        modal = self.data_entry_window

        # Başlık
        title_frame = ttk.Frame(modal, style='SubToolbar.TFrame')
        title_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(title_frame, text="\U0001f3af Gelişmiş Veri Giriş Sistemi",
                 font=('Segoe UI', 14, 'bold'),
                 background='#313244',
                 foreground='#89b4fa').pack(pady=10)

        # Form alanları
        form_frame = ttk.LabelFrame(modal, text="\U0001f4dd Kayıt Bilgileri", 
                                   padding=15, style='Card.TLabelframe')
        form_frame.pack(fill='x', pady=10, padx=15)

        # Grid düzeni
        fields = [
            ("\U0001f4c5 Tarih:", "date_entry"),
            ("\U0001f4cb Açıklama:", "desc_entry"),
            ("\U0001f4b0 Tutar:", "amount_entry"),
            ("\U0001f4c1 Dosya:", "file_entry")
        ]

        self.modal_entries = {}
        for i, (label, entry_key) in enumerate(fields):
            ttk.Label(form_frame, text=label,
                     font=('Segoe UI', 10, 'bold')).grid(row=i, column=0, 
                                                        sticky='w', pady=5)
            
            entry = ttk.Entry(form_frame, width=40, font=('Segoe UI', 10))
            entry.grid(row=i, column=1, sticky='ew', padx=(10, 0), pady=5)
            self.modal_entries[entry_key] = entry

        form_frame.columnconfigure(1, weight=1)

        # Kontrol butonları
        control_frame = ttk.Frame(modal)
        control_frame.pack(fill='x', pady=15, padx=15)

        buttons = [
            ("\U0001f4be Kaydet", self.save_advanced_record, "Success.TButton"),
            ("\U0001f9f9 Temizle", self.clear_advanced_form, "Secondary.TButton"),
            ("\U0001f4ca Göster", self.show_current_data, "Primary.TButton"),
            ("\u274c Kapat", self.close_modal, "Secondary.TButton")
        ]

        for text, command, style in buttons:
            btn = ttk.Button(control_frame, text=text, command=command,
                           style=style, width=12)
            btn.pack(side='left', padx=5)

        # İlerleme ve durum
        progress_frame = ttk.Frame(modal)
        progress_frame.pack(fill='x', pady=10, padx=15)

        ttk.Label(progress_frame, text="\U0001f4c8 İşlem İlerlemesi:",
                 font=('Segoe UI', 9, 'bold')).pack(anchor='w')

        self.modal_progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.modal_progress.pack(fill='x', pady=5)

        self.modal_status = ttk.Label(progress_frame, text="\U0001f7e1 Hazır - Kayıt girişi bekliyor",
                                     font=('Segoe UI', 9),
                                     foreground='#f9e2af')
        self.modal_status.pack(anchor='w', pady=5)
        
    # === MODAL FONKSİYONLARI ===
    
    def save_advanced_record(self):
        """Düzeltilmiş kayıt kaydetme - doğru sayılarla"""
        # Form verilerini al
        data = {}
        for key, entry in self.modal_entries.items():
            data[key] = entry.get().strip()
            
        if not all(data.values()):
            self.show_modal_warning("Uyarı", "Lütfen tüm alanları doldurun!")
            return
            
        try:
            amount_val = float(data['amount_entry'].replace(',', '.'))
        except ValueError:
            self.show_modal_error("Hata", "Geçersiz tutar formatı!")
            return
            
        # Ana tabloya ekle
        record_id = len(self.main_data) + 1
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        self.main_data.append({
            'id': record_id,
            'date': data['date_entry'],
            'file': data['file_entry'],
            'description': data['desc_entry'],
            'amount': amount_val,
            'status': 'Kaydedildi',
            'time': timestamp
        })
        
        # Ana tabloyu güncelle
        self.main_tree.insert('', 'end', values=[
            record_id, data['date_entry'], data['file_entry'],
            data['desc_entry'], f"{amount_val:.2f} TL",
            'Kaydedildi', timestamp
        ])
        
        # Dashboard güncellemesi
        self.update_dashboard_stats()
        
        # Progress güncelle - DÜZELTME: Doğru toplam sayı
        total_expected = len(self.current_records) if self.current_records else 100
        current_progress = len(self.main_data)
        progress_percent = min(100, (current_progress / total_expected) * 100)
        self.modal_progress['value'] = progress_percent

        # DÜZELTME: Modal üstünde başarı pop-up'ı
        self.show_modal_success(
            "Başarılı",
            f"Kayıt {record_id} kaydedildi!\n({current_progress}/{total_expected})"
        )

        # Form temizle
        self.clear_advanced_form()
        
        # Ana tabloya scroll
        children = self.main_tree.get_children()
        if children:
            self.main_tree.see(children[-1])
            
        # Dashboard highlight efekti
        if hasattr(self, 'total_transactions_label'):
            self.total_transactions_label.config(foreground='#a6e3a1')
            self.root.after(1000, lambda: self.total_transactions_label.config(foreground='black'))
            
    def clear_advanced_form(self):
        """Gelişmiş formu temizle"""
        for entry in self.modal_entries.values():
            entry.delete(0, tk.END)
        self.modal_status.config(
            text="\U0001f7e1 Form temizlendi - yeni kayıt girişi hazır",
            foreground='#f9e2af'
        )
        
    def show_current_data(self):
        """Mevcut veriyi göster"""
        if not self.current_records:
            messagebox.showinfo("Bilgi", "Gösterilecek veri bulunamadı.")
            return
            
        preview = tk.Toplevel(self.data_entry_window)
        preview.title("\U0001f4ca Yüklenen Veriler")
        preview.geometry("800x600")
        
        # Veri tablosu
        if self.current_records:
            columns = list(self.current_records[0].keys())
            tree = ttk.Treeview(preview, columns=columns, show="headings", height=20)
            
            for col in columns:
                tree.heading(col, text=col.title())
                tree.column(col, width=150, anchor="w")
                
            for rec in self.current_records:
                tree.insert("", "end", values=[rec.get(col, "") for col in columns])
                
            tree.pack(fill="both", expand=True, padx=15, pady=15)
            
        ttk.Button(preview, text="Kapat", command=preview.destroy).pack(pady=10)
        
    def close_modal(self):
        """Modal'ı kapat"""
        if self.data_entry_window:
            self.data_entry_window.destroy()
            self.data_entry_window = None
        self.update_process_status("\U0001f7e1 Veri giriş sistemi kapatıldı")

    def show_modal_success(self, title: str, message: str):
        """Modal üstünde başarı mesajı"""
        popup = tk.Toplevel(self.data_entry_window)
        popup.title(title)
        popup.geometry("350x150")
        popup.configure(bg='#2E3440')

        modal_x = self.data_entry_window.winfo_rootx()
        modal_y = self.data_entry_window.winfo_rooty()
        popup.geometry(f"350x150+{modal_x + 50}+{modal_y + 50}")

        popup.transient(self.data_entry_window)
        popup.attributes('-topmost', True)
        popup.lift()
        popup.focus_set()

        tk.Label(popup, text="✅", font=('Segoe UI', 24),
                 bg='#2E3440', fg='#a6e3a1').pack(pady=10)
        tk.Label(popup, text=message, font=('Segoe UI', 11),
                 bg='#2E3440', fg='#cdd6f4', justify='center').pack(pady=5)
        tk.Button(popup, text="Tamam", command=popup.destroy,
                  bg='#89b4fa', fg='#1e1e2e', font=('Segoe UI', 10, 'bold')).pack(pady=10)
        popup.after(2000, popup.destroy)

    def show_modal_warning(self, title: str, message: str):
        """Modal üstünde uyarı mesajı"""
        popup = tk.Toplevel(self.data_entry_window)
        popup.title(title)
        popup.geometry("300x120")
        popup.configure(bg='#2E3440')

        modal_x = self.data_entry_window.winfo_rootx()
        modal_y = self.data_entry_window.winfo_rooty()
        popup.geometry(f"300x120+{modal_x + 70}+{modal_y + 70}")

        popup.transient(self.data_entry_window)
        popup.attributes('-topmost', True)
        popup.grab_set()
        popup.lift()

        tk.Label(popup, text="⚠️", font=('Segoe UI', 20),
                 bg='#2E3440', fg='#f9e2af').pack(pady=5)
        tk.Label(popup, text=message, font=('Segoe UI', 10),
                 bg='#2E3440', fg='#cdd6f4').pack(pady=5)
        tk.Button(popup, text="Tamam", command=popup.destroy,
                  bg='#f38ba8', fg='#1e1e2e').pack(pady=5)

    def show_modal_error(self, title: str, message: str):
        """Modal üstünde hata mesajı"""
        popup = tk.Toplevel(self.data_entry_window)
        popup.title(title)
        popup.geometry("300x120")
        popup.configure(bg='#2E3440')

        modal_x = self.data_entry_window.winfo_rootx()
        modal_y = self.data_entry_window.winfo_rooty()
        popup.geometry(f"300x120+{modal_x + 70}+{modal_y + 70}")

        popup.transient(self.data_entry_window)
        popup.attributes('-topmost', True)
        popup.grab_set()
        popup.lift()

        tk.Label(popup, text="❌", font=('Segoe UI', 20),
                 bg='#2E3440', fg='#f38ba8').pack(pady=5)
        tk.Label(popup, text=message, font=('Segoe UI', 10),
                 bg='#2E3440', fg='#cdd6f4').pack(pady=5)
        tk.Button(popup, text="Tamam", command=popup.destroy,
                  bg='#f38ba8', fg='#1e1e2e').pack(pady=5)
        
    # === YARDIMCI FONKSİYONLAR ===
    
    def update_dashboard_stats(self):
        """Dashboard istatistiklerini güncelle"""
        if hasattr(self, 'total_transactions_label'):
            total = len(self.main_data)
            today = len([r for r in self.main_data 
                        if r['date'] == datetime.now().strftime('%d.%m.%Y')])
            
            self.total_transactions_label.config(text=str(total))
            if hasattr(self, 'today_transactions_label'):
                self.today_transactions_label.config(text=str(today))
                
    def update_process_status(self, message):
        """Süreç durumunu güncelle"""
        if hasattr(self, 'process_status_label'):
            self.process_status_label.config(text=message)
        self.update_status(message)
        
    def update_status(self, message):
        """Ana durum çubuğunu güncelle"""
        self.status_label.config(text=f"\U0001f503 {message}")
        self.root.update_idletasks()

    def _show_info_left(self, title: str, message: str) -> None:
        """Sol tarafta bilgi kutusu göster"""
        popup = tk.Toplevel(self.data_entry_window)
        popup.title(title)
        ttk.Label(popup, text=message).pack(padx=20, pady=10)
        ttk.Button(popup, text="Tamam", command=popup.destroy).pack(pady=5)
        popup.update_idletasks()
        x = self.data_entry_window.winfo_rootx() - popup.winfo_width() - 10
        y = self.data_entry_window.winfo_rooty()
        popup.geometry(f"+{x}+{y}")
        popup.transient(self.data_entry_window)
        popup.grab_set()
        popup.wait_window()

    def _ask_yes_no_left(self, title: str, message: str) -> bool:
        """Sol tarafta yes/no sor"""
        popup = tk.Toplevel(self.data_entry_window)
        popup.title(title)
        ttk.Label(popup, text=message).pack(padx=20, pady=10)
        result = {"val": False}

        def yes():
            result["val"] = True
            popup.destroy()

        def no():
            popup.destroy()

        btn_frame = ttk.Frame(popup)
        btn_frame.pack(pady=5)
        ttk.Button(btn_frame, text="Evet", command=yes).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Hayır", command=no).pack(side="left", padx=5)
        popup.update_idletasks()
        x = self.data_entry_window.winfo_rootx() - popup.winfo_width() - 10
        y = self.data_entry_window.winfo_rooty()
        popup.geometry(f"+{x}+{y}")
        popup.transient(self.data_entry_window)
        popup.grab_set()
        popup.wait_window()
        return result["val"]
        
    # === EVENT HANDLERs ===
    
    def tab_changed(self, event):
        """Sekme değişim eventi"""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        self.update_status(f"Aktif modül: {selected_tab}")
        
    def menu_selected(self, module, sub_menu):
        """Menü seçim eventi"""
        self.update_status(f"Menü: {module} > {sub_menu}")
        
        # Finans-Tahsilat menüsü seçilirse ilgili sekmeye git
        if "Finans" in module and "Tahsilat" in sub_menu:
            self.notebook.select(2)  # Finans sekmesi
            
    # === HIZLI ERİŞİM FONKSİYONLARI ===
    
    def go_home(self):
        """Ana sayfaya git"""
        self.notebook.select(0)
        self.update_status("\U0001f3e0 Ana sayfa")
        
    def open_dashboard(self):
        """Dashboard aç"""
        self.notebook.select(0)
        self.update_status("\U0001f4ca Dashboard açıldı")
        
    def quick_save(self):
        """Hızlı kaydet"""
        self.update_status("\U0001f4be Hızlı kaydetme...")
        messagebox.showinfo("Bilgi", "Veriler kaydedildi!")
        
    def quick_search(self):
        """Hızlı arama"""
        search_term = simpledialog.askstring("\U0001f50d Hızlı Arama", "Aranacak terimi girin:")
        if search_term:
            self.update_status(f"\U0001f50d Arama: '{search_term}'")
            
    def quick_print(self):
        """Hızlı yazdır"""
        self.update_status("\U0001f5a8\ufe0f Yazdırma...")
        messagebox.showinfo("Bilgi", "Yazdırma işlemi başlatıldı!")
        
    # === ANA FONKSİYON ===
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.update_status("\U0001f680 Enterprise ERP Sistemi hazır - Karmaşık navigasyon aktif")
        self.root.mainloop()
        
    # === EXTERNAL ACCESS ===
    
    def get_data_entry_button_action(self):
        """RPA için Veri Giriş butonunun fonksiyonu"""
        return self.step5_start_data_entry
        
    def get_main_data(self):
        """Ana veri listesini döndür"""
        return self.main_data
        
    def set_current_records(self, records):
        """Mevcut kayıtları ayarla"""
        self.current_records = records
        
    def set_processing_files(self, file_list):
        """İşlenecek dosya listesini ayarla"""
        self.processing_files = file_list

# Test
if __name__ == "__main__":
    app = EnterpriseGUI()
    app.run()
