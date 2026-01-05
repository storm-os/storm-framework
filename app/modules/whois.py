# whois.py
import whois
import socket

from app.colors import C

# Definisikan simbol status
SYM_INFO = "💡"
SYM_ERROR = "❌"

def get_whois_info(target):
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

    print(f"{C.HEADER} \n--- WHOIS LOOKUP untuk {target} ({target_type}) ---")

    try:
        # Panggil fungsi Whois
        w = whois.whois(target)

        # 2. Tampilkan Informasi Penting
        print(f"{C.MENU}{SYM_INFO} Domain Name: {C.RESET}{w.domain_name}")
        print(f"{C.MENU}{SYM_INFO} Registrar:   {C.RESET}{w.registrar}")

        # Tanggal adalah informasi sensitif
        print(f"{C.MENU}{SYM_INFO} Created Date:{C.RESET}{w.creation_date}")
        print(f"{C.MENU}{SYM_INFO} Expiry Date: {C.RESET}{w.expiration_date}")

        # Informasi kontak (seringkali target Social Engineering)
        print(f"{C.MENU} \n[ Kontak & Server Info ]")
        print(f"{C.MENU} {SYM_INFO} Registrant Org:{C.RESET}{w.org}")
        print(f"{C.MENU} {SYM_INFO} Admin Email:   {C.RESET}{w.emails}")
        print(f"{C.MENU} {SYM_INFO} Name Servers:  {C.RESET}{w.name_servers}")


    except Exception as e:
        # Menangani kesalahan jika domain tidak ditemukan atau ada masalah koneksi
        print(f"{C.ERROR} {SYM_ERROR} Error: Tidak dapat mengambil data Whois.")
        print(f"{C.ERROR} {SYM_ERROR} Detail: {e}")

    print(f"{C.HEADER} ---------------------------------------------")
