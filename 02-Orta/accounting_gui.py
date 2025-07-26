import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from datetime import datetime

class AdvancedAccountingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Muhasebe Pro - Gelişmiş Sistem")
        self.root.geometry("1400x800")
        self.root.state('zoomed')
        
        # Veri depolama
        self.main_data = []  # Ana tablodaki kayıtlar
        self.current_records = []  # Excel'den okunan kayıtlar
        
        # GUI'yi öne getir
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        
        self.setup_styles()
        self.create_dashboard()
        
    def setup_styles(self):
        """Profesyonel ve renkli stil"""
        style = ttk.Style()
        style.theme_use('clam')

        # Modern mavi-yeşil tema
        style.configure('Tab.TNotebook', tabposition='n', background='#2E3440')
        style.configure('Tab.TNotebook.Tab',
                       padding=[15, 8],
                       background='#4C566A',
                       foreground='white',
                       focuscolor='none')
        style.map('Tab.TNotebook.Tab',
                  background=[('selected', '#5E81AC')],
                  foreground=[('selected', 'white')])

        # Toolbar stili
        style.configure('Toolbar.TFrame',
                       background='#ECEFF4',
                       relief='flat')

        # Dashboard kartları
        style.configure('Card.TLabelframe',
                       background='#ECEFF4',
                       foreground='#2E3440',
                       borderwidth=2,
                       relief='solid')
        style.configure('Card.TLabelframe.Label',
                       background='#ECEFF4',
                       foreground='#2E3440',
                       font=('Arial', 10, 'bold'))

        # Butonlar
        style.configure('Action.TButton',
                       background='#5E81AC',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none')
        style.map('Action.TButton',
                  background=[('active', '#81A1C1')])
        
    def create_dashboard(self):
        """Ana dashboard ekranı"""
        # Üst menü çubuğu
        self.create_main_menu()
        
        # Sekme yapısı
        self.create_tab_system()
        
        # Ana içerik alanı
        self.create_main_content()
        
        # Status bar
        self.create_status_bar()
        
    def create_main_menu(self):
        """Üst menü çubuğu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Ana menüler - Presto benzeri
        menus = ["Muhasebe", "Gider", "Bütçe", "Finans-Ödeme", "Finans-Tahsilat", 
                "Satış", "Stok", "Üretim", "Personel", "Sabit Kıymet", "Hesap Tablosu", "Diğer"]
        
        for menu_name in menus:
            menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label=menu_name, menu=menu)
            menu.add_command(label=f"{menu_name} İşlemleri", 
                           command=lambda m=menu_name: self.menu_clicked(m))
    
    def create_tab_system(self):
        """Sekme sistemi"""
        # Ana frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Notebook (sekmeler)
        self.notebook = ttk.Notebook(main_frame, style='Tab.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Dashboard sekmesi
        self.dashboard_frame = ttk.Frame(self.notebook, style='Dashboard.TFrame')
        self.notebook.add(self.dashboard_frame, text="📊 Dashboard")
        
        # Finans-Tahsilat sekmesi
        self.finans_frame = ttk.Frame(self.notebook, style='Dashboard.TFrame')
        self.notebook.add(self.finans_frame, text="💰 Finans-Tahsilat")
        
        # Diğer sekmeler
        for name in ["📈 Raporlar", "⚙️ Ayarlar", "📋 Yardım"]:
            frame = ttk.Frame(self.notebook)
            self.notebook.add(frame, text=name)
        
        # Sekme değişimi eventi
        self.notebook.bind("<<NotebookTabChanged>>", self.tab_changed)
        
    def create_main_content(self):
        """Ana içerik alanları"""
        # Dashboard içeriği
        self.create_dashboard_content()
        
        # Finans-Tahsilat içeriği  
        self.create_finans_content()
        
    def create_dashboard_content(self):
        """Dashboard sekmesi içeriği"""
        # Başlık
        title_frame = ttk.Frame(self.dashboard_frame)
        title_frame.pack(fill='x', pady=10)
        
        ttk.Label(title_frame, text="🏠 Ana Dashboard", 
                 font=('Arial', 16, 'bold')).pack(side='left')
        
        # Bilgi kartları
        info_frame = ttk.Frame(self.dashboard_frame)
        info_frame.pack(fill='x', pady=20, padx=20)
        
        # Kart 1: Toplam İşlemler
        card1 = ttk.LabelFrame(info_frame, text="Toplam İşlemler", 
                               padding=20, style='Card.TLabelframe')
        card1.pack(side='left', fill='both', expand=True, padx=10)
        
        self.total_transactions_label = ttk.Label(card1, text="0", 
                                                 font=('Arial', 24, 'bold'))
        self.total_transactions_label.pack()
        
        # Kart 2: Bugünkü İşlemler  
        card2 = ttk.LabelFrame(info_frame, text="Bugünkü İşlemler", 
                               padding=20, style='Card.TLabelframe')
        card2.pack(side='left', fill='both', expand=True, padx=10)
        
        self.today_transactions_label = ttk.Label(card2, text="0", 
                                                 font=('Arial', 24, 'bold'))
        self.today_transactions_label.pack()
        
        # Ana tablo (tüm kayıtlar)
        self.create_main_table()
        
    def create_finans_content(self):
        """Finans-Tahsilat sekmesi içeriği"""
        # Başlık ve toolbar
        header_frame = ttk.Frame(self.finans_frame)
        header_frame.pack(fill='x', pady=10, padx=20)
        
        ttk.Label(header_frame, text="💰 Finans - Tahsilat İşlemleri", 
                 font=('Arial', 14, 'bold')).pack(side='left')
        
        # Küçük butonlar toolbar'ı
        toolbar_frame = ttk.Frame(self.finans_frame, style='Toolbar.TFrame', height=50)
        toolbar_frame.pack(fill='x', padx=20, pady=5)
        toolbar_frame.pack_propagate(False)
        
        # Küçük butonlar
        buttons = [
            ("📄 Yeni", self.new_entry),
            ("📂 Veri Giriş", self.open_data_entry),  # ANA BUTON!
            ("🔍 Ara", self.search_records),
            ("📊 Filtre", self.filter_records),
            ("🖨️ Yazdır", self.print_records),
            ("📤 Dışa Aktar", self.export_records)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(toolbar_frame, text=text, command=command, width=12)
            btn.pack(side='left', padx=5, pady=5)
        
        # Finans içerik alanı
        content_frame = ttk.Frame(self.finans_frame)
        content_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        ttk.Label(content_frame, text="Veri Giriş butonuna tıklayarak işlemleri başlatın.", 
                 font=('Arial', 12)).pack(pady=50)
                 
    def create_main_table(self):
        """Ana kayıt tablosu"""
        table_frame = ttk.Frame(self.dashboard_frame)
        table_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Tablo başlığı
        ttk.Label(table_frame, text="📋 Tüm İşlem Kayıtları", 
                 font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0, 10))
        
        # Treeview
        columns = ['ID', 'Tarih', 'Açıklama', 'Tutar', 'Durum', 'Zaman']
        self.main_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Sütun ayarları
        widths = [50, 100, 400, 120, 100, 150]
        for i, (col, width) in enumerate(zip(columns, widths)):
            self.main_tree.heading(col, text=col)
            self.main_tree.column(col, width=width, anchor='center' if i in [0, 1, 4, 5] else 'w')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.main_tree.yview)
        self.main_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack
        self.main_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
    def create_status_bar(self):
        """Alt durum çubuğu"""
        status_frame = ttk.Frame(self.root, relief='sunken', height=25)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)
        
        self.status_label = ttk.Label(status_frame, text="Hazır - Dashboard", 
                                     font=('Arial', 9))
        self.status_label.pack(side='left', padx=10, pady=3)
        
        # Sağ taraf
        time_label = ttk.Label(status_frame, 
                              text=f"Kullanıcı: Admin | {datetime.now().strftime('%d.%m.%Y %H:%M')}")
        time_label.pack(side='right', padx=10, pady=3)
        
    def tab_changed(self, event):
        """Sekme değiştirme eventi"""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        self.update_status(f"Aktif sekme: {selected_tab}")
        
    def menu_clicked(self, menu_name):
        """Menü tıklama eventi"""
        self.update_status(f"Menü seçildi: {menu_name}")
        if menu_name == "Finans-Tahsilat":
            self.notebook.select(1)  # Finans sekmesine geç
        
    def new_entry(self):
        """Yeni kayıt"""
        self.update_status("Yeni kayıt oluşturuluyor...")
        messagebox.showinfo("Bilgi", "Yeni kayıt özelliği henüz geliştirilmemiş.")
        
    def open_data_entry(self):
        """Veri Giriş modal'ını aç - SAĞ TARAFA KONUMLA"""
        self.update_status("Veri Giriş penceresi açılıyor...")

        # Modal pencere oluştur
        self.data_entry_window = tk.Toplevel(self.root)
        self.data_entry_window.title("📊 Veri Giriş Sistemi")
        self.data_entry_window.geometry("500x350")

        # Sağ tarafa konumla
        screen_width = self.root.winfo_screenwidth()
        x_position = screen_width - 520
        y_position = 100
        self.data_entry_window.geometry(f"500x350+{x_position}+{y_position}")

        self.data_entry_window.transient(self.root)
        # grab_set() kaldır - Dashboard'ı engellesin

        # Modal içeriği
        self.create_data_entry_modal()
        
    def create_data_entry_modal(self):
        """Modal içeriği - KÜÇÜK VE KOMPAKT"""
        modal = self.data_entry_window

        # Başlık - daha küçük
        title_frame = ttk.Frame(modal)
        title_frame.pack(fill='x', pady=5, padx=10)

        ttk.Label(title_frame, text="📊 Veri Giriş",
                 font=('Arial', 12, 'bold')).pack()

        # Form - kompakt
        form_frame = ttk.LabelFrame(modal, text="İşlem", padding=10)
        form_frame.pack(fill='x', pady=5, padx=10)

        # Alanlar - daha küçük
        ttk.Label(form_frame, text="📅").grid(row=0, column=0, sticky='w')
        self.date_entry = ttk.Entry(form_frame, width=20, font=('Arial', 9))
        self.date_entry.grid(row=0, column=1, sticky='ew', padx=5)

        ttk.Label(form_frame, text="📝").grid(row=1, column=0, sticky='w')
        self.desc_entry = ttk.Entry(form_frame, width=20, font=('Arial', 9))
        self.desc_entry.grid(row=1, column=1, sticky='ew', padx=5)

        ttk.Label(form_frame, text="💰").grid(row=2, column=0, sticky='w')
        self.amount_entry = ttk.Entry(form_frame, width=20, font=('Arial', 9))
        self.amount_entry.grid(row=2, column=1, sticky='ew', padx=5)

        form_frame.columnconfigure(1, weight=1)

        # Butonlar - küçük
        button_frame = ttk.Frame(modal)
        button_frame.pack(fill='x', pady=5, padx=10)

        self.save_btn = ttk.Button(button_frame, text="💾", command=self.save_current_record,
                                  style='Action.TButton', width=8)
        self.save_btn.pack(side='left', padx=2)

        self.clear_btn = ttk.Button(button_frame, text="🧹", command=self.clear_form,
                                   style='Action.TButton', width=8)
        self.clear_btn.pack(side='left', padx=2)

        # Durum - küçük
        self.modal_status = ttk.Label(modal, text="Hazır",
                                     font=('Arial', 8), foreground='blue')
        self.modal_status.pack(pady=5)
        
    def save_current_record(self):
        """Mevcut kaydı kaydet"""
        # Form verilerini al
        date_val = self.date_entry.get().strip()
        desc_val = self.desc_entry.get().strip()
        amount_val = self.amount_entry.get().strip()
        
        if not all([date_val, desc_val, amount_val]):
            messagebox.showwarning("Uyarı", "Lütfen tüm alanları doldurun!")
            return
            
        try:
            amount_float = float(amount_val.replace(',', '.'))
        except ValueError:
            messagebox.showerror("Hata", "Geçersiz tutar formatı!")
            return
            
        # Ana tabloya ekle
        record_id = len(self.main_data) + 1
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        self.main_data.append({
            'id': record_id,
            'date': date_val,
            'description': desc_val,
            'amount': amount_float,
            'status': 'Kaydedildi',
            'time': timestamp
        })
        
        # Ana tabloyu güncelle
        self.main_tree.insert('', 'end', values=[
            record_id, date_val, desc_val, f"{amount_float:.2f} TL",
            'Kaydedildi', timestamp
        ])
        print(f"DEBUG: main_tree children: {len(self.main_tree.get_children())}")
        
        # Dashboard'u güncelle
        self.update_dashboard_stats()

        # Tablo en alta scroll et (yeni kayıt görünsün)
        children = self.main_tree.get_children()
        if children:
            self.main_tree.see(children[-1])

        # Dashboard'ı highlight et (0.5 saniye)
        self.total_transactions_label.config(foreground='#A3BE8C')
        self.root.after(500, lambda: self.total_transactions_label.config(foreground='black'))

        # Form temizle
        self.clear_form()
        
        # Durum güncellemesi
        self.modal_status.config(text=f"✅ Kayıt {record_id} başarıyla kaydedildi!", 
                                foreground='green')
        self.update_status(f"Yeni kayıt eklendi: ID {record_id}")
        
    def clear_form(self):
        """Formu temizle"""
        self.date_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.modal_status.config(text="Form temizlendi - yeni veri girişi hazır", 
                                foreground='blue')
        
    def update_dashboard_stats(self):
        """Dashboard istatistiklerini güncelle"""
        total = len(self.main_data)
        today = len([r for r in self.main_data if r['date'] == datetime.now().strftime('%d.%m.%Y')])
        
        self.total_transactions_label.config(text=str(total))
        self.today_transactions_label.config(text=str(today))
        
    def search_records(self):
        """Kayıt arama"""
        self.update_status("Arama özelliği henüz geliştirilmemiş.")
        
    def filter_records(self):
        """Kayıt filtreleme"""
        self.update_status("Filtreleme özelliği henüz geliştirilmemiş.")
        
    def print_records(self):
        """Kayıtları yazdır"""
        self.update_status("Yazdırma özelliği henüz geliştirilmemiş.")
        
    def export_records(self):
        """Kayıtları dışa aktar"""
        self.update_status("Dışa aktarma özelliği henüz geliştirilmemiş.")

    def show_data(self):
        """Yüklenen Excel verilerini göster"""
        if not self.current_records:
            messagebox.showinfo("Bilgi", "Gösterilecek veri bulunamadı.")
            return

        preview = tk.Toplevel(self.root)
        preview.title("Yüklenen Veriler")

        columns = list(self.current_records[0].keys())
        tree = ttk.Treeview(preview, columns=columns, show="headings", height=15)
        for col in columns:
            tree.heading(col, text=col.title())
            tree.column(col, width=150, anchor="w")
        for rec in self.current_records:
            tree.insert("", "end", values=[rec.get(col, "") for col in columns])
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(preview, text="Kapat", command=preview.destroy).pack(pady=5)
        
    def update_status(self, message):
        """Durum çubuğunu güncelle"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def run(self):
        """Uygulamayı çalıştır"""
        self.update_status("Muhasebe Pro Hazır - Dashboard")
        self.root.mainloop()

# Test
if __name__ == "__main__":
    app = AdvancedAccountingGUI()
    app.run()
