# subdomain.py
import requests

from app.colors import C

# Subdomain list sederhana untuk pengujian
# Dalam pentest nyata, list ini bisa berisi ribuan kata
SUBDOMAINS = [
    "www", "dev", "api", "mail", "blog", "test", "staging",
    "admin", "ftp", "vpn", "server", "cms"
]

SYM_FOUND = "🟢"
SYM_NOT_FOUND = "⚫"

REQUIRED_OPTIONS = {
        "URL"           : ""
    }

def execute(options):
    """Mencari subdomain aktif dari domain target menggunakan list kata."""

    target_domain = options.get("URL")

    # Menghapus 'http://' atau 'https://' jika ada
    target_domain = target_domain.replace('http://', '').replace('https://', '').strip('/')

    print(f"{C.HEADER} \n--- SUBDOMAIN ENUMERATION untuk {target_domain} ---")

    # Jumlah subdomain ditemukan
    found_count = 0

    for subdomain in SUBDOMAINS:
        url = f"http://{subdomain}.{target_domain}"

        try:
            # Mengirim permintaan HEAD (lebih cepat karena tidak mengunduh konten)
            response = requests.head(url, timeout=3, allow_redirects=True)
            status_code = response.status_code

            # Status 200 (OK), 301/302 (Redirect), 403 (Forbidden) seringkali berarti host aktif
            if status_code < 400 or status_code == 403:
                # Menggunakan warna SUCCESS untuk subdomain yang ditemukan
                print(f"{C.SUCCESS}{SYM_FOUND} Subdomain Ditemukan: {url} [Status: {status_code}]")
                found_count += 1
            # Tidak perlu menampilkan status 404/5xx

        except requests.exceptions.RequestException:
            # Timeout, DNS error, atau Connection refused
            # Kita tidak menampilkan error, tapi kita bisa menampilkan status NOT FOUND
            pass

    if found_count == 0:
        print(f"{C.ERROR} Tidak ada subdomain aktif yang ditemukan dengan list sederhana ini.")

    print(f"{C.HEADER} -------------------------------------------------")
