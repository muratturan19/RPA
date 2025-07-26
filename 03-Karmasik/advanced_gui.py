import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class ComplexGUI:
    """Karmaşık bir Tkinter arayüzü"""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Karmaşık Muhasebe Sistemi")
        self.root.geometry("1200x700")
        self.status_var = tk.StringVar(value="Hazır")
        self._create_menus()
        self._create_widgets()

    def _create_menus(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        menu_names = [
            "Dosya", "Muhasebe", "Finans", "Raporlar",
            "Ayarlar", "Yardım", "Ekstra"
        ]
        for name in menu_names:
            menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label=name, menu=menu)
            menu.add_command(
                label=f"{name} Seçenek 1",
                command=lambda n=name: self.menu_clicked(n)
            )
            menu.add_command(
                label=f"{name} Seçenek 2",
                command=lambda n=name: self.menu_clicked(n)
            )

    def _create_widgets(self) -> None:
        self.progress = ttk.Progressbar(self.root, mode="determinate")
        self.progress.pack(fill="x", pady=10, padx=10)
        self.status_label = ttk.Label(self.root, textvariable=self.status_var)
        self.status_label.pack(anchor="w", padx=10)
        ttk.Button(
            self.root,
            text="İş Akışını Başlat",
            command=self.start_flow
        ).pack(pady=20)

    def menu_clicked(self, name: str) -> None:
        messagebox.showinfo("Menü", f"{name} menüsü seçildi")

    def start_flow(self) -> None:
        steps = [
            "Giriş",
            "Firma Seçimi",
            "Modül Seçimi",
            "Finans",
            "Tahsilat",
            "Veri Giriş",
            "Onay"
        ]
        choice = simpledialog.askstring(
            "Firma", "Firma adını girin", parent=self.root
        )
        if not choice:
            messagebox.showwarning("Uyarı", "Firma seçilmedi")
            return
        for i, step in enumerate(steps, 1):
            self.status_var.set(f"Adım {i}/{len(steps)}: {step}")
            self.progress['value'] = i / len(steps) * 100
            self.root.update()
            self.root.after(300)
            messagebox.showinfo("Adım", f"{step} adımı tamamlandı")
        self.status_var.set("Akış tamamlandı")

    def update_status(self, message: str) -> None:
        self.status_var.set(message)
        self.root.update_idletasks()

    def run(self) -> None:
        self.root.mainloop()

if __name__ == "__main__":
    app = ComplexGUI()
    app.run()
