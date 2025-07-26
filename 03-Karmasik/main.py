from __future__ import annotations

from pathlib import Path
import threading

from advanced_gui import ComplexGUI
from rpa_bot import EnterpriseRPABot


def run_rpa_with_gui(excel_paths: list[Path], progress_callback=None):
    gui = ComplexGUI()
    bot = EnterpriseRPABot(gui)

    def start_bot():
        bot.run(excel_paths, progress_callback)
        gui.update_status("RPA tamamlandı")

    gui.root.after(1000, start_bot)
    gui.run()
    return bot.get_results()


def start_gui_only() -> None:
    app = ComplexGUI()
    app.run()


def start_both_default() -> None:
    data_dir = Path("../Data")
    files = list(data_dir.glob("*.xlsx"))
    run_rpa_with_gui(files)


def main() -> None:
    while True:
        print("\n" + "=" * 60)
        print("KARMAŞIK RPA SİSTEMİ")
        print("=" * 60)
        print("1) Sadece GUI'yi başlat")
        print("2) GUI + RPA başlat (Data klasöründeki tüm Excel'ler)")
        print("0) Çıkış")
        choice = input("Seçiminiz: ").strip()
        if choice == "1":
            start_gui_only()
        elif choice == "2":
            start_both_default()
        elif choice == "0":
            break
        else:
            print("Geçersiz seçim")


if __name__ == "__main__":
    main()
