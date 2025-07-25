import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import re
from pathlib import Path

DEFAULT_PATTERN = r'^POSH.*MUSLUOĞLU$'


class PrestoGUI(tk.Tk):
    """Presto tarz\u0131 gelismis arayuz"""

    def __init__(self) -> None:
        super().__init__()
        self.title("Presto GUI")
        self.geometry("900x600")
        self.data = pd.DataFrame()
        self._build_widgets()

    def _build_widgets(self) -> None:
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=5)

        self.btn_load = ttk.Button(top, text="Excel Se\u00e7", command=self.load_excel)
        self.btn_load.pack(side="left")

        ttk.Label(top, text="Filtre Regex").pack(side="left", padx=5)
        self.pattern_var = tk.StringVar(value=DEFAULT_PATTERN)
        self.entry_pattern = ttk.Entry(top, textvariable=self.pattern_var, width=40)
        self.entry_pattern.pack(side="left")

        self.btn_filter = ttk.Button(top, text="Filtrele", command=self.apply_filter)
        self.btn_filter.pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=(), show="headings")
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def load_excel(self) -> None:
        """Excel dosyas\u0131n\u0131 se\u00e7 ve g\u00f6ster"""
        file_path = filedialog.askopenfilename(
            initialdir=Path(__file__).resolve().parents[1] / "data",
            title="Excel Dosyas\u0131 Se\u00e7",
            filetypes=[("Excel", "*.xlsx *.xls")],
        )
        if not file_path:
            return
        try:
            self.data = pd.read_excel(file_path)
            self.show_table(self.data)
            messagebox.showinfo("Bilgi", f"{len(self.data)} sat\u0131r y\u00fcklendi")
        except Exception as exc:
            messagebox.showerror("Hata", f"Excel okunamad\u0131: {exc}")

    def show_table(self, df: pd.DataFrame) -> None:
        """Tabloda veriyi g\u00f6ster"""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def apply_filter(self) -> None:
        """Girilen regex'e g\u00f6re s\u00fcz"""
        if self.data.empty:
            messagebox.showwarning("Uyar\u0131", "\u00d6nce Excel y\u00fckleyin")
            return
        pattern = self.pattern_var.get().strip()
        try:
            filt = self.data[self.data["A\u00e7\u0131klama"].str.match(pattern, na=False)]
            messagebox.showinfo("Sonu\u00e7", f"{len(filt)} sat\u0131r eslesme")
            self.show_table(filt)
        except re.error as exc:
            messagebox.showerror("Hata", f"Regex hatas\u0131: {exc}")
        except Exception as exc:
            messagebox.showerror("Hata", f"Filtreleme hatas\u0131: {exc}")


if __name__ == "__main__":
    app = PrestoGUI()
    app.mainloop()
