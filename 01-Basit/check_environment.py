#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RPA Öğrenme Projesi - Ortam Kontrol ve Kurulum Scripti
Her platformda çalışmasını garantiler
"""

import sys
import subprocess
import importlib.util
from pathlib import Path


def check_python_version():
    """Python versiyonunu kontrol eder"""
    print("🐍 Python Versiyonu Kontrolü:")
    version = sys.version_info
    print(f"   Mevcut versiyon: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ gereklidir!")
        return False
    else:
        print("✅ Python versiyonu uygun")
        return True


def check_package(package_name, import_name=None):
    """Bir paketi kontrol eder ve eksikse kurulum önerir"""
    if import_name is None:
        import_name = package_name

    try:
        spec = importlib.util.find_spec(import_name)
        if spec is not None:
            module = importlib.import_module(import_name)
            version = getattr(module, '__version__', 'bilinmiyor')
            print(f"✅ {package_name}: {version}")
            return True
        else:
            print(f"❌ {package_name}: BULUNAMADI")
            return False
    except Exception as e:
        print(f"❌ {package_name}: HATA - {e}")
        return False


def install_package(package):
    """Paketi otomatik kurar"""
    try:
        print(f"📦 {package} kuruluyor...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--user", "--quiet"])
        print(f"✅ {package} başarıyla kuruldu")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ {package} kurulumunda hata!")
        return False


def create_directories():
    """Gerekli klasörleri oluşturur"""
    directories = ["../data", "logs"]
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"📁 {dir_name} klasörü hazır")


def main():
    """Ana kontrol fonksiyonu"""
    print("🤖 RPA Öğrenme Projesi - Ortam Kontrolü")
    print("=" * 50)

    # Python versiyon kontrolü
    if not check_python_version():
        input("Enter'a basarak çıkın...")
        return

    print("\n📦 Gerekli Kütüphaneler Kontrolü:")

    # Gerekli paketler
    required_packages = [
        ("pandas", "pandas"),
        ("openpyxl", "openpyxl"),
        ("colorama", "colorama")
    ]

    missing_packages = []

    # Her paketi kontrol et
    for package, import_name in required_packages:
        if not check_package(package, import_name):
            missing_packages.append(package)

    # Eksik paketleri kur
    if missing_packages:
        print(f"\n⚠️  {len(missing_packages)} paket eksik. Otomatik kurulum başlıyor...")

        for package in missing_packages:
            if not install_package(package):
                print(f"\n❌ {package} kurulunamadı. Manuel kurulum gerekli:")
                print(f"   pip install {package}")
                input("Enter'a basarak devam edin...")
                return

        # Kurulumdan sonra tekrar kontrol
        print("\n🔄 Kurulum sonrası kontrol:")
        for package, import_name in required_packages:
            check_package(package, import_name)

    # Klasörleri oluştur
    print("\n📁 Klasör Yapısı:")
    create_directories()

    print("\n🎉 TÜM KONTROLLER BAŞARILI!")
    print("\nŞimdi çalıştırabilirsiniz:")
    print("  python create_real_data.py")
    print("  python main.py")

    input("\nEnter'a basarak devam edin...")


if __name__ == "__main__":
    main()
