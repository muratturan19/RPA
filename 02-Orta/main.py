"""Entry point for the intermediate RPA example."""

from __future__ import annotations

import threading

from rpa_bot import AdvancedRPABot


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

    bot = AdvancedRPABot()
    bot.set_gui_reference(gui_app)
    bot.run()


def start_bot_threaded() -> threading.Thread | None:
    """Run the RPA bot in a separate thread."""
    global gui_app

    if gui_app is None:
        print("\u274C Önce GUI'yi açın")
        return None

    bot = AdvancedRPABot()
    bot.set_gui_reference(gui_app)
    return bot.run()


def start_both() -> None:
    """Start both the GUI and the RPA bot."""
    global gui_app

    print("\U0001F5A5\ufe0f GUI başlatılıyor...")
    from accounting_gui import AdvancedAccountingGUI

    gui_app = AdvancedAccountingGUI()

    # GUI'yi öne getir ve odakla
    gui_app.root.lift()  # Pencereyi öne getir
    gui_app.root.attributes('-topmost', True)  # En üstte tut
    gui_app.root.after(100, lambda: gui_app.root.attributes('-topmost', False))  # 100ms sonra normal mod
    gui_app.root.focus_force()  # Odağı zorla

    # RPA'yı biraz gecikmeyle başlat ki GUI tam yüklensin
    gui_app.root.after(2000, start_bot_threaded)  # 2 saniye sonra RPA başlat

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
