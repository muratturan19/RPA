"""Tkinter GUI uygulaması."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class BankGUI(tk.Tk):
    """Banka işlemleri giriş arayüzü."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Banka İşlemleri Giriş Sistemi")
        self.geometry("800x600")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        self._create_widgets()

    def _create_widgets(self) -> None:
        frame = ttk.Frame(self)
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

        self.btn_cikis = ttk.Button(button_frame, text="Çıkış", command=self.destroy)
        self.btn_cikis.pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("Tarih", "Açıklama", "Tutar", "Hesap"), show="headings")
        for col in ("Tarih", "Açıklama", "Tutar", "Hesap"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

        for i in range(2):
            frame.columnconfigure(i, weight=1)

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
        self.temizle()

    def temizle(self) -> None:
        """Alanları temizle."""
        self.entry_tarih.delete(0, tk.END)
        self.entry_aciklama.delete(0, tk.END)
        self.entry_tutar.delete(0, tk.END)
        self.entry_hesap.delete(0, tk.END)
        self.entry_hesap.insert(0, "6232011")
