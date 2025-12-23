# main.py
import os
import requests

from app.update import run_update

from script.scanner import scan_target
from script.web_head import check_web_headers
from script.whois import get_whois_info
from script.dns import enumerate_dns_records
from script.subdomain import enumerate_subdomains
from script.credential_checker import check_default_credentials
from script.firebase_db import firebase_write_exploit_db
from script.firebase_fs import firestore_write_exploit
from script.md5_crypt import crack_shadow_hash
from script.osint import run_osint

from colorama import Fore, Style, init
init(autoreset=True) # Inisialisasi Colorama dan reset warna otomatis

# Dictionary Warna Global
C = {
    "HEADER": Fore.MAGENTA + Style.BRIGHT,
    "MENU": Fore.CYAN,
    "INPUT": Fore.YELLOW,
    "SUCCESS": Fore.GREEN + Style.BRIGHT,
    "ERROR": Fore.RED + Style.BRIGHT,
    "RESET": Style.RESET_ALL
}

# --- Fungsi Clear Screen ---

def clear_screen():
    """Membersihkan layar terminal"""
    # Fungsi Win
    if os.name == 'nt':
       os.system('cls')
    # Fungsi Linux
    else:
       os.system('clear')

# --- Akhir fungsi clear screen ---

# --- Cek update ---

# 1. Tentukan versi lokal tools saat ini
CURRENT_VERSION = "1.0.0"

def check_update():
    # URL mentah ke file version.txt di GitHub
    url = "https://raw.githubusercontent.com/Proot9/El-Cyber_Pentest/main/version.txt"
    try:
        response = requests.get(url, timeout=5)
        latest_version = response.text.strip()

        # Jika versi di GitHub lebih tinggi dari versi lokal
        if latest_version > CURRENT_VERSION:
            print(C["SUCCESS"] + f"\n[!] Update tersedia: v{latest_version} (Versi Anda: v{CURRENT_VERSION})" + C["RESET"])
    except:
        pass

# --- Akhir fungsi cek update ---

# --- Fungsi Menu ---

def tampilkan_menu():
    """Menampilkan pilihan menu utama dengan warna."""
    print(C["HEADER"] + "\n######################################")
    print(C["HEADER"] + "  TOOL KEAMANAN PYTHON V1.0 ")
    print(C["HEADER"] + "######################################")
    print(C["MENU"] + "1. Jalankan Port Scanner Cepat")
    print(C["MENU"] + "2. Scan Header Website")
    print(C["MENU"] + "3. Whois Lookup")
    print(C["MENU"] + "4. DNS Enumeration")
    print(C["MENU"] + "5. Subdomain Enumeration")
    print(C["MENU"] + "6. OSINT")
    print(C["ERROR"] + "99. Keluar")
    print(C["ERROR"] + "100. Update Tools")
    print(C["HEADER"] + "--------------------------------------")

    print(C["HEADER"] + "\n######################################")
    print(C["HEADER"] + "  TOOL ATTACKER PYTHON V1.0 ")
    print(C["HEADER"] + "######################################")
    print(C["MENU"] + "C1. BruteForce (Network)")
    print(C["MENU"] + "C2. BruteForce (MD5-Crypt)")
    print(C["MENU"] + "C3. Firebase Exploit FS")
    print(C["MENU"] + "C4. Firebase Exploit DB")
    print(C["HEADER"] + "--------------------------------------")

def main():
    clear_screen()

    while True:
        tampilkan_menu()
        check_update()

        # Menerapkan warna pada prompt input
        pilihan = input(C["INPUT"] + "Masukkan pilihan Anda: " + C["RESET"])

        if pilihan == '1':
            target = input(C["INPUT"] + "Masukkan IP Target: " + C["RESET"])

            # Panggil Fungsi
            scan_target(target, C)

        elif pilihan == '2':
            url_target = input(C["INPUT"] + "Masukkan URL Target: " + C["RESET"])

            # Panggil Fungsi
            check_web_headers(url_target, C)

        elif pilihan == '3':
            whois_target = input(C["INPUT"] + "Masukkan Domain/IP Target: " + C["RESET"])

            # Panggil Fungsi
            get_whois_info(whois_target, C)

        elif pilihan == '4':
            dns_target = input(C["INPUT"] + "Masukkan Domain Target: " + C["RESET"])

            # Panggil Fungsi
            enumerate_dns_records(dns_target, C)

        elif pilihan == '5':
            subdomain_target = input(C["INPUT"] + "Masukkan Domain Target: " + C["RESET"])

            # Panggil Fungsi
            enumerate_subdomains(subdomain_target, C)

        elif pilihan == '6':
            osint_target = input(C["INPUT"] + "Masukkan Email Target: " + C["RESET"])

            # Panggil Fungsi
            run_osint(osint_target, C)

        elif pilihan.upper() == 'C1':
            credential_target = input(C["INPUT"] + "Masukkan IP Target: " + C["RESET"])
            credential_port = input(C["INPUT"] + "Masukkan PORT: " + C["RESET"])
            pass_path = input(C["INPUT"] + "Masukkan Path Pass: " + C["RESET"])

            # Panggil Fungsi
            check_default_credentials(credential_target, C, credential_port, pass_path)

        elif pilihan.upper() == 'C2':
            hash_target = input(C["INPUT"] + "Masukkan Hash Target: " + C["RESET"])
            path_pw = input(C["INPUT"] + "Masukkan Path Pass: " + C["RESET"])

            # Panggil Fungsi
            crack_shadow_hash(hash_target, path_pw, C)

        elif pilihan.upper() == 'C3':

            # Panggil Fungsi
            firestore_write_exploit(C)

        elif pilihan.upper() == 'C4':

            # Panggil Fungsi
            firebase_write_exploit_db(C)

        elif pilihan == '99':
            print(C["SUCCESS"] + "Terima kasih, sampai jumpa!")
            break

        elif pilihan == '100':
            run_update(C)

        else:
            print(C["ERROR"] + "Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
