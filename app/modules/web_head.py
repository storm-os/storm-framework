# web_head.py
import requests

from app.colors import C

# Definisikan simbol status (tanpa warna)
SYM_EXPOSED = "❗"
SYM_WARNING = "⚠️"
SYM_ERROR = "❌"

def check_web_headers(target_url):
    """Memeriksa header keamanan sebuah URL."""

    # 1. Pastikan URL memiliki skema (http:// atau https://)
    if not target_url.startswith(('https://', 'http://')):
        target_url = 'https://' + target_url

    # Menggunakan warna HEADER untuk garis pemisah
    print(f"{C.HEADER} \n--- MEMERIKSA HEADER: {target_url} ---")

    try:
        # Mengirim permintaan GET
        response = requests.get(target_url, timeout=5)

        # 2. Iterasi (Loop) melalui setiap Header yang diterima
        # Menggunakan warna MENU untuk Header dan nilai
        print(f"{C.MENU} Headers Diterima:")
        for header, value in response.headers.items():
            # Membuat Header (kunci) menjadi lebih menonjol (misalnya menggunakan HEADER/ERROR)
            print(f"  {C.HEADER}{header}:{C.RESET} {value}")

        # 3. Validasi Keamanan
        print(f"{C.HEADER} \n--- ANALISIS KEAMANAN HEADER ---")

        # Cek Header 'Server' (seringkali diekspos)
        server_header = response.headers.get('Server')
        if server_header:
            # Menggunakan warna ERROR untuk peringatan eksposur
            print(f"{C.ERROR}{SYM_EXPOSED} Server Version Exposed: {server_header}{C.RESET}")
        else:
            # Menggunakan warna SUCCESS jika header tidak ada (seringkali lebih aman)
            print(f"{C.SUCCESS}Server header tidak ditemukan atau tersembunyi. (Baik){C.RESET}")


        # Cek Header Keamanan X-Frame-Options (Pencegahan Clickjacking)
        if 'X-Frame-Options' not in response.headers:
            # Menggunakan warna ERROR untuk peringatan keamanan
            print(f"{C.ERROR}{SYM_WARNING} Header X-Frame-Options HILANG. Potensi Clickjacking.{C.RESET}")
        else:
             # Menggunakan warna SUCCESS jika header ada
             print(f"{C.SUCCESS}X-Frame-Options: {response.headers.get('X-Frame-Options')}. (Aman){C.RESET}")

        # Contoh Cek Tambahan: Strict-Transport-Security (Pencegahan Downgrade)
        if 'Strict-Transport-Security' not in response.headers and target_url.startswith('https://'):
             print(f"{C.ERROR}{SYM_WARNING} Header Strict-Transport-Security HILANG. Risiko Downgrade HTTP.{C.RESET}")
        else:
             print(f"{C.SUCCESS}HSTS ditemukan atau tidak berlaku (HTTP).{C.RESET}")

    except requests.exceptions.RequestException as e:
        # Menggunakan warna ERROR untuk pesan kegagalan
        print(f"{C.ERROR}{SYM_ERROR} Error saat koneksi ke {target_url}: {e}{C.RESET}")

    print(f"{C.HEADER} ---------------------------------------")
