"""Uygulama başlangıç noktası."""

from __future__ import annotations

import sys
import tkinter as tk
from typing import Callable

GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"

from gui_app import BankGUI
from rpa_bot import RPABot
from data_reader import DataReader


def start_gui() -> BankGUI:
    """GUI uygulamasını başlat."""
    app = BankGUI()
    return app


def start_bot() -> None:
    """RPA botu başlat."""
    bot = RPABot()
    bot.run()


def show_data() -> None:
    """Test verilerini göster."""
    reader = DataReader()
    if reader.read_excel() and reader.validate_data():
        for row in reader.get_data():
            print(row)


def menu() -> None:
    """Kullanıcı menüsü."""
    def both() -> None:
        app = start_gui()
        app.after(500, start_bot)
        app.mainloop()

    options: dict[str, Callable[[], None]] = {
        "1": lambda: start_gui().mainloop(),
        "2": start_bot,
        "3": both,
        "4": show_data,
    }

    while True:
        print(f"{CYAN}\n1) Sadece GUI'yi başlat")
        print("2) Sadece RPA botu çalıştır")
        print("3) Her ikisini başlat")
        print("4) Test verilerini göster")
        print(f"0) Çıkış{RESET}")
        choice = input("Seçiminiz: ").strip()
        if choice == "0":
            sys.exit()
        action = options.get(choice)
        if action:
            action()
        else:
            print(f"{RED}Geçersiz seçim{RESET}")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\nProgram sonlandırıldı")
