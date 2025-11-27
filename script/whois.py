# whois.py

import whois
import socket

# Definisikan simbol status
SYM_INFO = "💡"
SYM_ERROR = "❌"

def get_whois_info(target, C):
    """Mengambil informasi Whois dari Domain/IP."""

    # Menghapus 'http://' atau 'https://' jika ada
    target = target.replace('http://', '').replace('https://', '').strip('/')

    # 1. Tentukan apakah target adalah IP atau Domain
    try:
        # Coba ubah target menjadi IP (jika berhasil, itu IP)
        socket.gethostbyname(target)
        target_type = "IP Address"
    except socket.error:
        target_type = "Domain"

    print(C["HEADER"] + f"\n--- WHOIS LOOKUP untuk {target} ({target_type}) ---")

    try:
        # Panggil fungsi Whois
        w = whois.whois(target)

        # 2. Tampilkan Informasi Penting
        print(C["MENU"] + f"{SYM_INFO} Domain Name: {C['RESET']}{w.domain_name}")
        print(C["MENU"] + f"{SYM_INFO} Registrar:   {C['RESET']}{w.registrar}")

        # Tanggal adalah informasi sensitif
        print(C["MENU"] + f"{SYM_INFO} Created Date:{C['RESET']}{w.creation_date}")
        print(C["MENU"] + f"{SYM_INFO} Expiry Date: {C['RESET']}{w.expiration_date}")

        # Informasi kontak (seringkali target Social Engineering)
        print(C["MENU"] + f"\n[ Kontak & Server Info ]")
        print(C["MENU"] + f"{SYM_INFO} Registrant Org:{C['RESET']}{w.org}")
        print(C["MENU"] + f"{SYM_INFO} Admin Email:   {C['RESET']}{w.emails}")
        print(C["MENU"] + f"{SYM_INFO} Name Servers:  {C['RESET']}{w.name_servers}")


    except Exception as e:
        # Menangani kesalahan jika domain tidak ditemukan atau ada masalah koneksi
        print(C["ERROR"] + f"{SYM_ERROR} Error: Tidak dapat mengambil data Whois.")
        print(C["ERROR"] + f"{SYM_ERROR} Detail: {e}")

    print(C["HEADER"] + "---------------------------------------------")
