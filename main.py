# main.py
import os
import requests

from app.update import run_update
from app.colors import C

from app.modules.scanner import scan_target
from app.modules.web_head import check_web_headers
from app.modules.whois import get_whois_info
from app.modules.dns import enumerate_dns_records
from app.modules.subdomain import enumerate_subdomains
from app.modules.attc_net import check_default_credentials
from app.modules.firebase_db import firebase_write_exploit_db
from app.modules.firebase_fs import firestore_write_exploit
from app.modules.md5_crypt import crack_shadow_hash
from app.modules.osint import run_osint

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
CURRENT_VERSION = "2.1.0"

def check_update():
    # URL mentah ke file version.txt di GitHub
    url = "https://raw.githubusercontent.com/Proot9/El-Cyber_Pentest/main/version.txt"
    try:
        response = requests.get(url, timeout=5)
        latest_version = response.text.strip()

        # Jika versi di GitHub lebih tinggi dari versi lokal
        if latest_version > CURRENT_VERSION:
            print(f"{C.HEADER}\n######################################")
            print(f"{C.SUCCESS}\n[!] Update tersedia: v{latest_version} (Versi Anda: v{CURRENT_VERSION})")
            print(f"{C.SUCCESS}\n[-] Ketik: npm update pentest")
            print(f"{C.HEADER}\n######################################")
    except:
        pass

# --- Akhir fungsi cek update ---

# --- Fungsi Menu ---

def tampilkan_menu():
    """Menampilkan pilihan menu utama dengan warna."""
    print(f"{C.HEADER}\n######################################")
    print(f"{C.HEADER}  TOOL KEAMANAN PYTHON  ")
    print(f"{C.HEADER}######################################")
    print(f"{C.MENU} 1. Jalankan Port Scanner Cepat")
    print(f"{C.MENU} 2. Scan Header Website")
    print(f"{C.MENU} 3. Whois Lookup")
    print(f"{C.MENU} 4. DNS Enumeration")
    print(f"{C.MENU} 5. Subdomain Enumeration")
    print(f"{C.MENU} 6. OSINT")
    print(f"{C.ERROR} 99. Keluar")
    print(f"{C.HEADER} --------------------------------------")

    print(f"{C.HEADER}\n######################################")
    print(f"{C.HEADER}  TOOL EXPLOIT PYTHON  ")
    print(f"{C.HEADER}######################################")
    print(f"{C.MENU} C1. BruteForce (Network)")
    print(f"{C.MENU} C2. BruteForce (MD5-Crypt)")
    print(f"{C.MENU} C3. Firebase Exploit FS")
    print(f"{C.MENU} C4. Firebase Exploit DB")
    print(f"{C.HEADER} --------------------------------------")

def main():
    clear_screen()

    while True:
        tampilkan_menu()
        check_update()

        # Menerapkan warna pada prompt input
        pilihan = input(f"{C.INPUT} Masukkan pilihan Anda: ")

        if pilihan == '1':
            target = input(f"{C.INPUT} Masukkan IP Target: ")

            # Panggil Fungsi
            scan_target(target)

        elif pilihan == '2':
            url_target = input(f"{C.INPUT} Masukkan URL Target: ")

            # Panggil Fungsi
            check_web_headers(url_target)

        elif pilihan == '3':
            whois_target = input(f"{C.INPUT} Masukkan Domain/IP Target: ")

            # Panggil Fungsi
            get_whois_info(whois_target)

        elif pilihan == '4':
            dns_target = input(f"{C.INPUT} Masukkan Domain Target: ")

            # Panggil Fungsi
            enumerate_dns_records(dns_target)

        elif pilihan == '5':
            subdomain_target = input(f"{C.INPUT} Masukkan Domain Target: ")

            # Panggil Fungsi
            enumerate_subdomains(subdomain_target)

        elif pilihan == '6':
            osint_target = input(f"{C.INPUT} Masukkan Email Target: ")

            # Panggil Fungsi
            run_osint(osint_target)

        elif pilihan.upper() == 'C1':
            credential_target = input(f"{C.INPUT} Masukkan IP Target: ")
            credential_port = input(f"{C.INPUT} Masukkan PORT: ")
            pass_path = input(f"{C.INPUT} Masukkan Path Pass: ")

            # Panggil Fungsi
            check_default_credentials(credential_target, credential_port, pass_path)

        elif pilihan.upper() == 'C2':
            hash_target = input(f"{C.INPUT} Masukkan Hash Target: ")
            path_pw = input(f"{C.INPUT} Masukkan Path Pass: ")

            # Panggil Fungsi
            crack_shadow_hash(hash_target, path_pw)

        elif pilihan.upper() == 'C3':

            # Panggil Fungsi
            firestore_write_exploit()

        elif pilihan.upper() == 'C4':

            # Panggil Fungsi
            firebase_write_exploit_db()

        elif pilihan == '99':
            print(f"{C.SUCCESS} Terima kasih, sampai jumpa!")
            break

        elif pilihan == 'npm update pentest':
            run_update()

        else:
            print(f"{C.ERROR} Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
