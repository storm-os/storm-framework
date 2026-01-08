import requests
from versi import VERSION
from app.utility.colors import C


def check_update():
    # URL mentah ke file version.txt di GitHub
    url = "https://raw.githubusercontent.com/Proot9/Cyber-Pentest/main/version.txt"
    try:
        response = requests.get(url, timeout=5)
        latest_version = response.text.strip()

        # Jika versi di GitHub lebih tinggi dari versi lokal
        if latest_version > VERSION:
            print(f"{C.HEADER}\n######################################")
            print(f"{C.SUCCESS}\n[!] Update available: v{latest_version} | Current version: v{VERSION}")
            print(f"{C.SUCCESS}\n[-] Type: update")
            print(f"{C.HEADER}\n######################################")
    except:
        pass
