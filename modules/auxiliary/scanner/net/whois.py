# whois.py
import whois
import socket

from app.utility.colors import C


REQUIRED_OPTIONS = {
        "DOMAIN"           : "",
        "IP"            : ""
    }

def execute(options):
    """Retrieving Whois information from Domain/IP"""

    target_url = options.get("DOMAIN")
    target_ip = options.get("IP")

    target = target_url if target_url else target_ip

    # Menghapus 'http://' atau 'https://' jika ada
    target = target.replace('http://', '').replace('https://', '').strip('/')

    # 1. Tentukan apakah target adalah IP atau Domain
    try:
        # Coba ubah target menjadi IP (jika berhasil, itu IP)
        socket.gethostbyname(target)
        target_type = "IP Address"
    except socket.error:
        target_type = "Domain"

    print(f"{C.HEADER}\n WHOIS LOOKUP For {target} ({target_type})")
 
    try:
        # Panggil fungsi Whois
        w = whois.whois(target)

        # 2. Tampilkan Informasi Penting
        print(f"{C.MENU} Domain Name:            {C.RESET}{w.domain_name}")
        print(f"{C.MENU} Registrar:              {C.RESET}{w.registrar}")

        # Tanggal adalah informasi sensitif
        print(f"{C.MENU} Created Date:           {C.RESET}{w.creation_date}")
        print(f"{C.MENU} Expiry Date:            {C.RESET}{w.expiration_date}")

        # Informasi kontak (seringkali target Social Engineering)
        print(f"{C.MENU} \n[ Contact & Server Info ]")
        print(f"{C.MENU} Registrant Organization:{C.RESET}{w.org}")
        print(f"{C.MENU} Email Admin:            {C.RESET}{w.emails}")
        print(f"{C.MENU} Name Servers:           {C.RESET}{w.name_servers}")

    except KeyboardInterrupt:
        return
    except Exception as e:
        # Menangani kesalahan jika domain tidak ditemukan atau ada masalah koneksi
        print(f"{C.ERROR} ERROR: Unable to retrieve Whois data.")
        print(f"{C.ERROR} Detail: {e}")

    print(f"{C.HEADER} ---------------------------------------------\n")
