from __future__ import annotations

from rpa_bot import RPABot


def main() -> None:
    while True:
        print("\n=== Orta Seviye RPA ===")
        print("1) RPA botunu çalıştır")
        print("0) Çıkış")
        choice = input("Seçiminiz: ").strip()
        if choice == "1":
            bot = RPABot()
            bot.run()
        elif choice == "0":
            break
        else:
            print("Geçersiz seçim")


if __name__ == "__main__":
    main()
