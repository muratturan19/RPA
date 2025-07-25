"""Entry point for the intermediate RPA example."""

from __future__ import annotations

import threading

from rpa_bot import RPABot


# Global GUI reference used by the bot
gui_app = None


def start_gui() -> None:
    """Launch only the GUI application."""
    global gui_app
    from accounting_gui import AdvancedAccountingGUI

    gui_app = AdvancedAccountingGUI()
    gui_app.run()


def start_bot() -> None:
    """Run the RPA bot if the GUI is available."""
    global gui_app

    if gui_app is None:
        print("\u274C Önce GUI'yi açın")
        return

    bot = RPABot()
    bot.run()


def start_bot_threaded() -> threading.Thread | None:
    """Run the RPA bot in a separate thread."""
    global gui_app

    if gui_app is None:
        print("\u274C Önce GUI'yi açın")
        return None

    bot = RPABot()
    thread = threading.Thread(target=bot.run, daemon=True)
    thread.start()
    return thread


def start_both() -> None:
    """Start both the GUI and the RPA bot."""
    global gui_app

    print("\U0001F5A5\ufe0f GUI başlatılıyor...")
    from accounting_gui import AdvancedAccountingGUI

    gui_app = AdvancedAccountingGUI()

    # Start the bot shortly after the GUI opens so the window remains responsive
    gui_app.root.after(100, start_bot_threaded)
    gui_app.run()


def main() -> None:
    """Main menu handling for the intermediate RPA example."""
    while True:
        print("\n=== Orta Seviye RPA ===")
        print("1) Sadece GUI'yi başlat")
        print("2) GUI açıksa RPA'yı çalıştır")
        print("3) Her ikisini başlat")
        print("0) Çıkış")
        choice = input("Seçiminiz: ").strip()
        if choice == "1":
            start_gui()
        elif choice == "2":
            start_bot()
        elif choice == "3":
            start_both()
        elif choice == "0":
            break
        else:
            print("Geçersiz seçim")


if __name__ == "__main__":
    main()
