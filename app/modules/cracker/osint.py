import requests
import time
import json

from app.colors import C

# --- Pengecekan Facebook ---
def check_facebook_email(email):
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
            return f"{C.SUCCESS} ✅ DITEMUKAN (Facebook): {email}{C.RESET}"
        else:
            return f"{C.ERROR} ❌ TIDAK DITEMUKAN (Facebook): {email}{C.RESET}"

    except requests.exceptions.RequestException as e:
        return f"{C.ERROR} 🚨 ERROR Koneksi/Timeout (Facebook): {e}{C.RESET}"
    except Exception as e:
        return f"{C.ERROR} 🚨 ERROR tak terduga (Facebook): {e}{C.RESET}"


# --- Pengecekan Instagram ---
def check_instagram_email(email):
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
            return f"{C.ERROR} ❌ TIDAK DITEMUKAN (Instagram): {email}{C.RESET}"

        # --- LOGIKA KEBERHASILAN (Berbasis Status/JSON) ---

        # Jika bukan string kegagalan, kita coba parse JSON untuk konfirmasi success/error lain
        try:
            data = response.json()

            # Jika ada objek 'user' atau status ok
            if data.get('status') == 'ok' or data.get('user') is not None:
                return f"{C.SUCCESS} ✅ DITEMUKAN (Instagram): {email}{C.RESET}"

        except json.JSONDecodeError:
            # Jika GAGAL decode JSON, dan tidak ada string kegagalan di atas,
            # ini berarti kita menerima HTML aneh yang BUKAN pesan "Tidak Ditemukan"
            return f"{C.ERROR} 🚨 ERROR: Respons non-JSON diterima (Blokir). Coba lagi nanti.{C.RESET}"

        # Jika berhasil di-decode JSON tapi tidak ada indikator sukses:
        return f"{C.ERROR} 🚨 ERROR: Respons tidak terduga/Diblokir oleh Instagram.{C.RESET}"

    except requests.exceptions.RequestException as e:
        return f"{C.ERROR} 🚨 ERROR Koneksi/Timeout (Instagram): {e}{C.RESET}"
    except Exception as e:
        return f"{C.ERROR} 🚨 ERROR tak terduga (Instagram): {e}{C.RESET}"


REQUIRED_OPTIONS = {
        "EMAIL"         : ""
    }


# --- Fungsi Utama Runner ---
def execute(options):
    """
    Fungsi utama untuk menjalankan pengecekan email tunggal di berbagai platform.
    """

    email = options.get("EMAIL")

    email_clean = email.strip()

    print(f"{C.HEADER} \n--- OSINT MULTI-PLATFORM EMAIL CHECKER ---")

    if not email_clean:
        print(f"{C.ERROR} [-] ERROR: Email kosong.")
        print(f"{C.HEADER} ------------------------------------------")
        return

    # Pemisah visual
    print(f"{C.MENU} \n===== MEMERIKSA {email_clean} =====")

    # 1. Jalankan Pengecekan Facebook
    print(f"{C.MENU} [*] Memeriksa Facebook...")
    result_fb = check_facebook_email(email_clean)
    print(result_fb)

    # 2. Jalankan Pengecekan Instagram
    print(f"{C.MENU} [*] Memeriksa Instagram...")
    result_ig = check_instagram_email(email_clean)
    print(result_ig)

    print(f"{C.HEADER} \n------------------------------------------")
