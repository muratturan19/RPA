"""Tkinter GUI uygulaması."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time


class BankGUI(tk.Tk):
    """Banka işlemleri giriş arayüzü."""

    # Bekleme süreleri (saniye)
    WAIT_AFTER_CLICK = 0.5
    WAIT_AFTER_TYPING = 0.2
    WAIT_AFTER_SAVE = 1.0

    def __init__(self) -> None:
        super().__init__()
        self.title("Menü / Dashboard")
        self.geometry("800x600")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self._create_dashboard()

        # Status bar
        self.status_frame = ttk.Frame(self)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_label = ttk.Label(self.status_frame, text="Hazır", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(side=tk.RIGHT, padx=5)

    # -------------------------------------- Dashboard
    def _create_dashboard(self) -> None:
        menu = ttk.Frame(self)
        menu.pack(padx=10, pady=10, fill="x")

        self.btn_banka_islemleri = ttk.Button(menu, text="Banka İşlemleri", command=self.open_form)
        self.btn_banka_islemleri.pack(side="left")

        # Ana tablo
        self.tree = ttk.Treeview(self, columns=("Tarih", "Açıklama", "Tutar", "Hesap"), show="headings")
        for col in ("Tarih", "Açıklama", "Tutar", "Hesap"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    # -------------------------------------- Form Popup
    def open_form(self) -> None:
        """Yeni işlem girişi için popup aç."""
        if hasattr(self, "form_window") and self.form_window and self.form_window.winfo_exists():
            self.form_window.lift()
            return

        self.form_window = tk.Toplevel(self)
        self.form_window.title("Banka İşlemi Girişi")
        self.form_window.grab_set()

        frame = ttk.Frame(self.form_window)
        frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(frame, text="Tarih").grid(row=0, column=0, sticky="w")
        self.entry_tarih = ttk.Entry(frame)
        self.entry_tarih.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame, text="Açıklama").grid(row=1, column=0, sticky="w")
        self.entry_aciklama = ttk.Entry(frame)
        self.entry_aciklama.grid(row=1, column=1, sticky="ew")

        ttk.Label(frame, text="Tutar").grid(row=2, column=0, sticky="w")
        self.entry_tutar = ttk.Entry(frame)
        self.entry_tutar.grid(row=2, column=1, sticky="ew")

        ttk.Label(frame, text="Hesap Kodu").grid(row=3, column=0, sticky="w")
        self.entry_hesap = ttk.Entry(frame)
        self.entry_hesap.insert(0, "6232011")
        self.entry_hesap.grid(row=3, column=1, sticky="ew")

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=5)

        self.btn_kaydet = ttk.Button(button_frame, text="Kaydet", command=self.kaydet)
        self.btn_kaydet.pack(side="left", padx=5)

        self.btn_temizle = ttk.Button(button_frame, text="Temizle", command=self.temizle)
        self.btn_temizle.pack(side="left", padx=5)

        self.btn_iptal = ttk.Button(button_frame, text="İptal", command=self._close_form)
        self.btn_iptal.pack(side="left", padx=5)

        for i in range(2):
            frame.columnconfigure(i, weight=1)

    def _close_form(self) -> None:
        if hasattr(self, "form_window") and self.form_window:
            self.form_window.destroy()
            self.form_window = None

    def kaydet(self) -> None:
        """Veriyi tabloya ekle."""
        tarih = self.entry_tarih.get().strip()
        aciklama = self.entry_aciklama.get().strip()
        tutar = self.entry_tutar.get().strip()
        hesap = self.entry_hesap.get().strip()

        if not (tarih and aciklama and tutar):
            messagebox.showerror("Hata", "Tüm alanları doldurun")
            return
        self.tree.insert("", "end", values=(tarih, aciklama, tutar, hesap))
        self._close_form()

    def temizle(self) -> None:
        """Alanları temizle."""
        self.entry_tarih.delete(0, tk.END)
        self.entry_aciklama.delete(0, tk.END)
        self.entry_tutar.delete(0, tk.END)
        self.entry_hesap.delete(0, tk.END)
        self.entry_hesap.insert(0, "6232011")

    def update_status(self, message: str, progress: float | None = None) -> None:
        """Status bar'ı günceller."""
        self.status_label.config(text=message)
        if progress is not None:
            self.progress_var.set(progress)
        self.update_idletasks()

    def run(self) -> None:
        """GUI'yi çalıştırır"""
        self.mainloop()

    # --- RPA integration
    def add_transaction_via_popup(self, row: dict[str, str | float]) -> None:
        """RPA için popup üzerinden kayıt ekler."""
        self.open_form()
        time.sleep(self.WAIT_AFTER_CLICK)

        self.entry_tarih.insert(0, str(row.get("Tarih", "")))
        time.sleep(self.WAIT_AFTER_TYPING)
        self.entry_aciklama.insert(0, str(row.get("Açıklama", "")))
        time.sleep(self.WAIT_AFTER_TYPING)
        self.entry_tutar.insert(0, str(row.get("Tutar", "")))
        time.sleep(self.WAIT_AFTER_TYPING)
        self.entry_hesap.delete(0, tk.END)
        self.entry_hesap.insert(0, "6232011")
        time.sleep(self.WAIT_AFTER_TYPING)

        self.kaydet()
        time.sleep(self.WAIT_AFTER_SAVE)

        self.update()  # arayüzü güncelle
