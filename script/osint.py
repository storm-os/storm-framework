import requests
import time
import json

# --- Pengecekan Facebook ---
def check_facebook_email(email, C):
    """
    Mengirim permintaan POST ke endpoint identifikasi Facebook.
    """
    url = "https://www.facebook.com/login/identify/?ctx=recover"
    payload = {'email': email}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': url,
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        response_text = response.text.lower()

        failure_strings = [
        "find your account",
        "temukan akun anda",
        "no search results"
        ]

        is_registered = not any(fs in response_text for fs in failure_strings)

        if is_registered:
            return C["SUCCESS"] + f"✅ DITEMUKAN (Facebook): {email}" + C["RESET"]
        else:
            return C["ERROR"] + f"❌ TIDAK DITEMUKAN (Facebook): {email}" + C["RESET"]

    except requests.exceptions.RequestException as e:
        return C["ERROR"] + f"🚨 ERROR Koneksi/Timeout (Facebook): {e}" + C["RESET"]
    except Exception as e:
        return C["ERROR"] + f"🚨 ERROR tak terduga (Facebook): {e}" + C["RESET"]


# --- Pengecekan Instagram ---
def check_instagram_email(email, C):
    """
    Mengirim permintaan POST ke endpoint recovery Instagram yang lebih sederhana, 
    dan secara spesifik mencari string kegagalan dari screenshot (HTML).
    """
    url = "https://www.instagram.com/accounts/account_recovery_send_ajax/"

    payload = {
        'email_or_username': email,
    }

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'X-CSRFToken': 'missing',
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'https://www.instagram.com/',
    }

    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)

        response_text = response.text

        # --- LOGIKA KUNCI KEGAGALAN (Berbasis String) ---
        # Mencari string kegagalan (dari kode Java dan screenshot)
        failure_strings = [
            "No users found",
            "No user found",
            # String dari pop-up screenshot Anda:
            "tidak bisa menemukan akun Anda",
            "tidak terhubung ke akun"
        ]

        if any(fs in response_text for fs in failure_strings):
            return C["ERROR"] + f"❌ TIDAK DITEMUKAN (Instagram): {email}" + C["RESET"]

        # --- LOGIKA KEBERHASILAN (Berbasis Status/JSON) ---

        # Jika bukan string kegagalan, kita coba parse JSON untuk konfirmasi success/error lain
        try:
            data = response.json()

            # Jika ada objek 'user' atau status ok
            if data.get('status') == 'ok' or data.get('user') is not None:
                return C["SUCCESS"] + f"✅ DITEMUKAN (Instagram): {email}" + C["RESET"]

        except json.JSONDecodeError:
            # Jika GAGAL decode JSON, dan tidak ada string kegagalan di atas,
            # ini berarti kita menerima HTML aneh yang BUKAN pesan "Tidak Ditemukan"
            return C["ERROR"] + f"🚨 ERROR: Respons non-JSON diterima (Blokir). Coba lagi nanti." + C["RESET"]

        # Jika berhasil di-decode JSON tapi tidak ada indikator sukses:
        return C["ERROR"] + f"🚨 ERROR: Respons tidak terduga/Diblokir oleh Instagram." + C["RESET"]

    except requests.exceptions.RequestException as e:
        return C["ERROR"] + f"🚨 ERROR Koneksi/Timeout (Instagram): {e}" + C["RESET"]
    except Exception as e:
        return C["ERROR"] + f"🚨 ERROR tak terduga (Instagram): {e}" + C["RESET"]





# --- Fungsi Utama Runner ---
def run_osint(email, C):
    """
    Fungsi utama untuk menjalankan pengecekan email tunggal di berbagai platform.
    """
    email_clean = email.strip()

    print(C["HEADER"] + "\n--- OSINT MULTI-PLATFORM EMAIL CHECKER ---" + C["RESET"])

    if not email_clean:
        print(C["ERROR"] + "[-] ERROR: Email kosong.")
        print(C["HEADER"] + "------------------------------------------" + C["RESET"])
        return

    # Pemisah visual
    print(C["MENU"] + f"\n===== MEMERIKSA {email_clean} =====" + C["RESET"])

    # 1. Jalankan Pengecekan Facebook
    print(C["MENU"] + f"[*] Memeriksa Facebook..." + C["RESET"])
    result_fb = check_facebook_email(email_clean, C)
    print(result_fb)

    # 2. Jalankan Pengecekan Instagram
    print(C["MENU"] + f"[*] Memeriksa Instagram..." + C["RESET"])
    result_ig = check_instagram_email(email_clean, C)
    print(result_ig)

    print(C["HEADER"] + "\n------------------------------------------" + C["RESET"])
