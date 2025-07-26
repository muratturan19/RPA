import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import re
from pathlib import Path
from datetime import datetime

class AdvancedAccountingGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Muhasebe Pro - Banka Hesap İzleme Sistemi")
        self.root.geometry("1400x800")
        self.root.state('zoomed')  # Tam ekran başlat

        self.data = pd.DataFrame()
        self.filtered_data = pd.DataFrame()

        # Stil ayarları
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Profesyonel stil ayarları"""
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Header.TFrame', background='#2E4BC6')
        style.configure('Toolbar.TFrame', background='#F0F0F0', relief='raised')
        style.configure('Status.TFrame', background='#E0E0E0', relief='sunken')

    def create_widgets(self):
        # Ana menü çubuğu
        self.create_menu_bar()

        # Toolbar (ikon çubuğu)
        self.create_toolbar()

        # Ana çalışma alanı
        self.create_main_area()

        # Status bar
        self.create_status_bar()

    def create_menu_bar(self):
        """Üst menü çubuğu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Ana menüler
        menus = [
            ("Muhasebe", ["Hesap Planı", "Yevmiye", "Mizan"]),
            ("Gider", ["Gider Fişi", "Gider Listesi"]),
            ("Bütçe", ["Bütçe Tanımı", "Bütçe Kontrolü"]),
            ("Finans-Ödeme", ["Ödeme Emri", "Çek Senedi"]),
            ("Finans-Tahsilat", ["Tahsilat Fişi", "Pos Tahsilat"]),
            ("Satış", ["Satış Faturası", "Satış Listesi"]),
            ("Stok", ["Stok Kartı", "Stok Hareketleri"]),
            ("Üretim", ["Üretim Emri", "Reçete"]),
            ("Personel", ["Personel Kartı", "Bordro"]),
            ("Diğer", ["Yedekleme", "Ayarlar"])
        ]

        for menu_name, items in menus:
            menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label=menu_name, menu=menu)
            for item in items:
                menu.add_command(label=item, command=lambda x=item: self.menu_action(x))

    def create_toolbar(self):
        """İkon çubuğu"""
        toolbar_frame = ttk.Frame(self.root, style='Toolbar.TFrame', height=80)
        toolbar_frame.pack(fill='x', padx=2, pady=2)
        toolbar_frame.pack_propagate(False)

        # Büyük ikonlar için butonlar
        buttons = [
            ("📄 Yeni Kayıt", self.new_record),
            ("📂 Excel Yükle", self.load_excel),
            ("🔍 Filtrele", self.show_filter_dialog),
            ("💾 Kaydet", self.save_data),
            ("📊 Rapor", self.generate_report),
            ("⚙️ Ayarlar", self.settings),
        ]

        for i, (text, command) in enumerate(buttons):
            btn = ttk.Button(toolbar_frame, text=text, command=command, width=12)
            btn.pack(side='left', padx=5, pady=10)

    def create_main_area(self):
        """Ana çalışma alanı"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill='both', padx=5, pady=5)

        # Filtre alanı (üst)
        self.create_filter_area(main_frame)

        # Tablo alanı (orta)
        self.create_table_area(main_frame)

        # Özet alanı (alt)
        self.create_summary_area(main_frame)

    def create_filter_area(self, parent):
        """Filtre kontrolları"""
        filter_frame = ttk.LabelFrame(parent, text="Filtre ve Arama Kriterleri", padding=10)
        filter_frame.pack(fill='x', pady=(0, 5))

        # İlk satır
        row1 = ttk.Frame(filter_frame)
        row1.pack(fill='x', pady=2)

        ttk.Label(row1, text="Başlangıç Tarihi:").pack(side='left', padx=5)
        self.date_start = ttk.Entry(row1, width=12)
        self.date_start.pack(side='left', padx=5)
        self.date_start.insert(0, "01.01.2025")

        ttk.Label(row1, text="Bitiş Tarihi:").pack(side='left', padx=5)
        self.date_end = ttk.Entry(row1, width=12)
        self.date_end.pack(side='left', padx=5)
        self.date_end.insert(0, "31.12.2025")

        ttk.Label(row1, text="Hesap No:").pack(side='left', padx=5)
        self.account_combo = ttk.Combobox(row1, width=20, values=[
            "6232011 - GARANTİ BANKASI",
            "1001001 - KASA",
            "1201001 - ALICILAR",
            "3201001 - SATIŞLAR"
        ])
        self.account_combo.pack(side='left', padx=5)

        # İkinci satır
        row2 = ttk.Frame(filter_frame)
        row2.pack(fill='x', pady=5)

        ttk.Label(row2, text="Açıklama Pattern:").pack(side='left', padx=5)
        self.pattern_var = tk.StringVar(value=r'^POSH.*\/\d{15}$')
        self.pattern_entry = ttk.Entry(row2, textvariable=self.pattern_var, width=30)
        self.pattern_entry.pack(side='left', padx=5)

        ttk.Label(row2, text="Min Tutar:").pack(side='left', padx=5)
        self.min_amount = ttk.Entry(row2, width=10)
        self.min_amount.pack(side='left', padx=5)

        ttk.Label(row2, text="Max Tutar:").pack(side='left', padx=5)
        self.max_amount = ttk.Entry(row2, width=10)
        self.max_amount.pack(side='left', padx=5)

        ttk.Button(row2, text="🔍 Filtrele", command=self.apply_advanced_filter).pack(side='left', padx=10)
        ttk.Button(row2, text="🔄 Temizle", command=self.clear_filters).pack(side='left', padx=5)

    def create_table_area(self, parent):
        """Ana tablo alanı"""
        table_frame = ttk.Frame(parent)
        table_frame.pack(expand=True, fill='both', pady=5)

        # Treeview ile scrollbar
        tree_frame = ttk.Frame(table_frame)
        tree_frame.pack(expand=True, fill='both')

        # Sütunlar - Professional muhasebe programı gibi çok sütunlu
        columns = [
            "Tarih", "Seri", "No", "Referans", "Kasa/Hesap",
            "Kasa/Hesap Kodu", "Hesap Adı", "Borç Tutarı",
            "Alacak Tutarı", "Döviz Türü", "Açıklama",
            "Yevmiye No", "Vade Tarihi", "Özel Kod"
        ]

        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=20)

        # Sütun ayarları
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            if col in ["Borç Tutarı", "Alacak Tutarı"]:
                self.tree.column(col, width=100, anchor='e')
            elif col in ["Tarih", "Vade Tarihi"]:
                self.tree.column(col, width=80, anchor='center')
            elif col in ["Seri", "No"]:
                self.tree.column(col, width=60, anchor='center')
            else:
                self.tree.column(col, width=120, anchor='w')

        # Scrollbar'lar
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid yerleştirme
        self.tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def create_summary_area(self, parent):
        """Alt özet bilgiler"""
        summary_frame = ttk.LabelFrame(parent, text="Özet Bilgiler", padding=10)
        summary_frame.pack(fill='x', pady=(5, 0))

        # Özet bilgileri için etiketler
        info_frame = ttk.Frame(summary_frame)
        info_frame.pack(fill='x')

        self.summary_labels = {}
        labels = [
            ("Toplam Kayıt:", "0"),
            ("Borç Toplamı:", "0.00 TL"),
            ("Alacak Toplamı:", "0.00 TL"),
            ("Net Bakiye:", "0.00 TL"),
            ("Seçili Kayıt:", "0"),
            ("Son Güncelleme:", datetime.now().strftime("%d.%m.%Y %H:%M"))
        ]

        for i, (label_text, value) in enumerate(labels):
            frame = ttk.Frame(info_frame)
            frame.pack(side='left', padx=15)

            ttk.Label(frame, text=label_text, font=('Arial', 9, 'bold')).pack()
            self.summary_labels[label_text] = ttk.Label(frame, text=value, font=('Arial', 10))
            self.summary_labels[label_text].pack()

    def create_status_bar(self):
        """Alt durum çubuğu"""
        status_frame = ttk.Frame(self.root, style='Status.TFrame', height=25)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)

        self.status_label = ttk.Label(status_frame, text="Hazır", font=('Arial', 9))
        self.status_label.pack(side='left', padx=10, pady=3)

        # Sağ taraf - kullanıcı bilgisi ve tarih
        right_frame = ttk.Frame(status_frame)
        right_frame.pack(side='right', padx=10, pady=3)

        ttk.Label(right_frame, text=f"Kullanıcı: Admin | {datetime.now().strftime('%d.%m.%Y %H:%M')}",
                 font=('Arial', 9)).pack()

    # Event handler metodları
    def menu_action(self, item):
        self.update_status(f"Menü seçildi: {item}")
        messagebox.showinfo("Bilgi", f"{item} özelliği henüz geliştirilmemiş.")

    def new_record(self):
        self.update_status("Yeni kayıt oluşturuluyor...")
        messagebox.showinfo("Bilgi", "Yeni kayıt özelliği henüz geliştirilmemiş.")

    def load_excel(self):
        """Excel dosyası yükleme"""
        file_path = filedialog.askopenfilename(
            title="Excel Dosyası Seç",
            filetypes=[("Excel dosyaları", "*.xlsx *.xls"), ("Tüm dosyalar", "*.*")]
        )

        if file_path:
            try:
                self.data = pd.read_excel(file_path)
                self.show_data(self.data)
                self.update_summary()
                self.update_status(f"Excel yüklendi: {len(self.data)} kayıt")
                messagebox.showinfo("Başarılı", f"{len(self.data)} kayıt yüklendi.")
            except Exception as e:
                messagebox.showerror("Hata", f"Excel dosyası yüklenemedi:\n{str(e)}")

    def show_filter_dialog(self):
        """Gelişmiş filtre penceresi"""
        self.update_status("Filtre penceresi açılıyor...")
        # Bu metodun içeriği geliştirilecek
        messagebox.showinfo("Bilgi", "Gelişmiş filtre özelliği yakında eklenecek.")

    def apply_advanced_filter(self):
        """Gelişmiş filtreleme - dinamik sütun bulma ile"""
        if self.data.empty:
            messagebox.showwarning("Uyarı", "Önce Excel dosyası yükleyin.")
            return

        try:
            filtered = self.data.copy()

            # Açıklama sütununu dinamik bul
            aciklama_cols = [col for col in filtered.columns if 'açıklama' in str(col).lower()]
            if aciklama_cols:
                aciklama_col = aciklama_cols[0]
                pattern = self.pattern_var.get().strip()
                if pattern:
                    filtered = filtered[filtered[aciklama_col].str.match(pattern, na=False)]

            # Tutar sütununu dinamik bul
            tutar_cols = [col for col in filtered.columns if 'tutar' in str(col).lower()]
            if tutar_cols:
                tutar_col = tutar_cols[0]
                min_val = self.min_amount.get().strip()
                max_val = self.max_amount.get().strip()

                if min_val:
                    filtered = filtered[filtered[tutar_col] >= float(min_val)]
                if max_val:
                    filtered = filtered[filtered[tutar_col] <= float(max_val)]

            self.filtered_data = filtered
            self.show_data(filtered)
            self.update_summary()
            self.update_status(f"Filtre uygulandı: {len(filtered)} kayıt")

        except Exception as e:
            messagebox.showerror("Hata", f"Filtreleme hatası:\n{str(e)}")

    def clear_filters(self):
        """Filtreleri temizle"""
        self.pattern_var.set(r'^POSH.*\/\d{15}$')
        self.min_amount.delete(0, tk.END)
        self.max_amount.delete(0, tk.END)
        self.account_combo.set('')

        if not self.data.empty:
            self.show_data(self.data)
            self.update_summary()

        self.update_status("Filtreler temizlendi")

    def show_data(self, df):
        """Veriyi tabloda göster"""
        # Mevcut verileri temizle
        for item in self.tree.get_children():
            self.tree.delete(item)

        if df.empty:
            return

        # Verileri tabloya ekle
        for index, row in df.iterrows():
            values = []
            for col in self.tree['columns']:
                if col in df.columns:
                    values.append(str(row[col]))
                else:
                    values.append('')
            self.tree.insert('', 'end', values=values)

    def update_summary(self):
        """Özet bilgileri güncelle"""
        if hasattr(self, 'filtered_data') and not self.filtered_data.empty:
            data = self.filtered_data
        else:
            data = self.data

        if data.empty:
            return

        # Temel istatistikler
        total_records = len(data)

        # Tutar sütununu dinamik bul
        tutar_cols = [col for col in data.columns if 'tutar' in str(col).lower()]
        if tutar_cols:
            tutar_col = tutar_cols[0]
            positive_sum = data[data[tutar_col] > 0][tutar_col].sum()
            negative_sum = abs(data[data[tutar_col] < 0][tutar_col].sum())
            net_balance = data[tutar_col].sum()

            self.summary_labels["Borç Toplamı:"].config(text=f"{positive_sum:,.2f} TL")
            self.summary_labels["Alacak Toplamı:"].config(text=f"{negative_sum:,.2f} TL")
            self.summary_labels["Net Bakiye:"].config(text=f"{net_balance:,.2f} TL")
        else:
            self.summary_labels["Borç Toplamı:"].config(text="0.00 TL")
            self.summary_labels["Alacak Toplamı:"].config(text="0.00 TL")
            self.summary_labels["Net Bakiye:"].config(text="0.00 TL")

        self.summary_labels["Toplam Kayıt:"].config(text=str(total_records))
        self.summary_labels["Son Güncelleme:"].config(text=datetime.now().strftime("%d.%m.%Y %H:%M"))

    def sort_by_column(self, col):
        """Sütuna göre sıralama"""
        self.update_status(f"Sıralanıyor: {col}")
        # Sıralama özelliği geliştirilecek

    def save_data(self):
        self.update_status("Veriler kaydediliyor...")
        messagebox.showinfo("Bilgi", "Kaydetme özelliği henüz geliştirilmemiş.")

    def generate_report(self):
        self.update_status("Rapor oluşturuluyor...")
        messagebox.showinfo("Bilgi", "Rapor özelliği henüz geliştirilmemiş.")

    def settings(self):
        self.update_status("Ayarlar açılıyor...")
        messagebox.showinfo("Bilgi", "Ayarlar penceresi henüz geliştirilmemiş.")

    def update_status(self, message):
        """Durum çubuğunu güncelle"""
        self.status_label.config(text=message)
        self.root.update_idletasks()

    def run(self):
        """Uygulamayı çalıştır"""
        self.update_status("Muhasebe Pro Hazır")
        self.root.mainloop()

# Test için
if __name__ == "__main__":
    app = AdvancedAccountingGUI()
    app.run()
