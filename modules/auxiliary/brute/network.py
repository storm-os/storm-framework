# credential_checker.py

import socket
import paramiko # Untuk SSH
import ftplib # Untuk FTP
import telnetlib # Untuk Telnet
import concurrent.futures
import requests
import os
import time

from assets.wordlist.userpass import DEFAULT_CREDS, COMMON_USERS
from app.utility.colors import C

SYM_SUCCESS = "🔑"
SYM_FAILED = "🔒"
SYM_ERROR = "❌"

# --- Fungsi Pengujian SSH ---
def test_ssh(target_ip, port, username, password):
    """Mencoba login SSH menggunakan Paramiko."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
        target_ip,
        port=port,
        username=username,
        password=password,
        timeout=2,
        banner_timeout=1.5
        )
        return True
    except paramiko.AuthenticationException:
        return False
    except paramiko.SSHException:
        return False
    except Exception:
        return False
    finally:
        client.close()

# --- Fungsi Pengujian FTP ---
def test_ftp(target_ip, port, username, password):
    """Mencoba login FTP menggunakan ftplib."""
    ftp = ftplib.FTP()
    try:
        ftp.connect(target_ip, port, timeout=2)
        ftp.login(username, password)
        return True
    except ftplib.all_errors:
        return False
    except socket.error:
        return False
    finally:
        try:
            ftp.quit()
        except:
            pass

# --- Fungsi Pengujian Telnet (BARU) ---
def test_telnet(target_ip, port, username, password):
    """
    Mencoba login Telnet menggunakan telnetlib dengan interaksi berbasis prompt.
    """
    try:
        # Koneksi dengan timeout singkat
        tn = telnetlib.Telnet(target_ip, port, timeout=2.5)

        # Cari prompt login (misalnya: "login:")
        tn.read_until(b"login: ", timeout=1)
        tn.write(username.encode('ascii') + b"\n")

        # Cari prompt password (misalnya: "Password:")
        tn.read_until(b"Password: ", timeout=1)
        tn.write(password.encode('ascii') + b"\n")

        # Baca sisa respons untuk mencari prompt shell ($ atau #)
        # Indikasi kuat bahwa login berhasil
        result = tn.read_until(b"$", timeout=1.5)
        result += tn.read_until(b"#", timeout=1.5)

        tn.close()

        # Verifikasi: Jika prompt shell ditemukan, anggap berhasil
        if b"$" in result or b"#" in result:
             return True
        else:
             return False

    except socket.timeout:
        # Timeout koneksi atau menunggu prompt
        return False
    except (socket.error, EOFError):
        # Kesalahan koneksi atau server menutup koneksi
        return False
    except Exception:
        # Kesalahan umum
        return False

# --- Fungsi Pengujian Grafana (DISINKRONKAN) ---
def test_grafana(target_ip, port, username, password):
    """Mencoba login Grafana menggunakan requests (HTTP POST)."""
    login_url = f"http://{target_ip}:{port}/login"

    # Payload yang dikirim sebagai JSON
    payload = {
        "user": username,
        "password": password
    }

    headers = {
        "Content-Type": "application/json"
    }

    try:
        # allow_redirects=False agar kita bisa menangkap kode 302 (tanda sukses login)
        response = requests.post(
            login_url,
            json=payload,
            headers=headers,
            timeout=3,
            allow_redirects=False
        )

        # Sukses Grafana: Kode 302 Found dan diarahkan ke /dashboard atau /
        # Kita memeriksa kode status dan header location
        if response.status_code == 302 and 'location' in response.headers and response.headers['location'].startswith('/'):
            return True
        else:
            return False

    except requests.exceptions.RequestException:
        # Menangani kesalahan koneksi atau timeout
        return False
    except Exception:
        return False

REQUIRED_OPTIONS = {
        "IP"            : "",
        "PORT"          : "",
        "PASS"          : ""
    }

# --- Fungsi Utama ---
def execute(options):
    """Menjalankan pengujian kredensial lemah pada layanan yang ditentukan."""

    target_ip = options.get("IP")
    target_ports = options.get("PORT")
    wordlist_path = options.get("PASS")

    print(f"{C.HEADER} \n--- CREDENTIAL CHECKER untuk {target_ip} ---")

    # Mapping Port ke Fungsi Pengujian
    ALL_SERVICES_MAPPING = {
        21: ("FTP", test_ftp),
        22: ("SSH", test_ssh),
        23: ("Telnet", test_telnet),
        3000: ("Grafana (Web)", test_grafana),
    }

    # ---------------------------------------------
    # Logika Penentuan Port Target
    # ---------------------------------------------
    ports_to_run = []

    if target_ports:
        # Jika port diberikan, parse port_string
        try:
            # Mengubah string "22,23,3000" menjadi list [22, 23, 3000]
            for p in target_ports.split(','):
                port_int = int(p.strip())
                if port_int in ALL_SERVICES_MAPPING:
                    ports_to_run.append(port_int)
                else:
                    print(f"{C.ERROR}  {SYM_ERROR} Port {port_int} tidak didukung oleh script ini. Melewati.")
        except ValueError:
             print(f"{C.ERROR}  {SYM_ERROR} Format port tidak valid. Gunakan format '22,23,3000'.")
             return
    else:
        # Jika target_ports tidak diberikan, gunakan semua port default
        print(f"{C.MENU}  [!] Port tidak ditentukan. Menggunakan semua port default (21, 22, 23, 3000).")
        ports_to_run = list(ALL_SERVICES_MAPPING.keys())

    if not ports_to_run:
        print(f"{C.ERROR}  {SYM_ERROR} Tidak ada port yang valid untuk diuji. Keluar.")
        return

    # ---------------------------------------------
    # Proses Pengujian
    # ---------------------------------------------
    for port in ports_to_run:
        service_name, test_function = ALL_SERVICES_MAPPING[port]

        print(f"{C.MENU} \n{service_name} (Port {port}) Analisis:")

        # Cek apakah port terbuka sebelum mencoba brute force (Tetap dipertahankan)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((target_ip, port)) != 0:
            print(f"{C.ERROR}  {SYM_ERROR} Port {port} {service_name} tampaknya tertutup. Melewati.")
            s.close()
            continue
        s.close()

        # --- Lanjutkan dengan Tahap 1 dan Tahap 2 yang sudah ada ---

        # ---------------------------------------------
        # Tahap 1: Coba Kredensial Default Tetap
        # ---------------------------------------------
        # (Salin semua kode Tahap 1 dari script lama Anda ke sini)
        print(f"{C.MENU}  [*] Memulai Tahap 1: Kredensial Default...")
        found_weak_creds = False

        for user, passwd in DEFAULT_CREDS:
            try:
                if test_function(target_ip, port, user, passwd):
                    print(f"{C.SUCCESS}  {SYM_SUCCESS} LOGIN BERHASIL! ({service_name}) -> U:{user} P:{passwd}")
                    found_weak_creds = True
                    break
                else:
                    print(f"{C.MENU}  {SYM_FAILED} GAGAL: {user}:{passwd}")

            except (ConnectionError, TimeoutError):
                print(f"{C.ERROR} [!] Koneksi terputus/Timeout. Menghentikan target ini...")
                break
            except Exception as e:
                print(f"{C.ERROR} [!] Error Fatal: {e}")
                break

        if found_weak_creds:
            continue

        # ---------------------------------------------
        # Tahap 2: Coba Brute Force dengan Wordlist Dinamis
        # ---------------------------------------------
        # (Salin semua kode Tahap 2 dari script lama Anda ke sini)
        if wordlist_path and os.path.exists(wordlist_path):
            print(f"{C.MENU}  [*] Memulai Tahap 2: Brute Force dengan {wordlist_path}...")

            try:
                with open(wordlist_path, 'r', encoding='latin-1') as f:
                    for target_user in COMMON_USERS:
                        f.seek(0) # Kembali ke awal file wordlist untuk setiap user baru
                        for line in f:
                            passwd = line.strip()
                            if not passwd:
                                continue

                            if test_function(target_ip, port, target_user, passwd):
                                print(f"{C.SUCCESS} \n  {SYM_SUCCESS} LOGIN BERHASIL! ({service_name}) -> U:{target_user} P:{passwd}")
                                return # Hentikan proses total jika berhasil

                            # Tampilkan kemajuan di baris yang sama (\r)
                            print(f"{C.MENU}  [>] Mencoba: U:{target_user:<20}P:{passwd:<20}", end='\r', flush=True)

                    print(f"{C.MENU} \n[!] Brute Force selesai tanpa menemukan kredensial yang cocok.")

            except FileNotFoundError:
                print(f"{C.ERROR}  {SYM_ERROR} ERROR: File Wordlist tidak ditemukan di {wordlist_path}.")
            except Exception as e:
                print(f"{C.ERROR}  {SYM_ERROR} ERROR tak terduga saat Brute Force: {e}")
                break
        elif wordlist_path:
             print(f"{C.MENU}  [!] Tahap 2 dilewati. Wordlist Path diberikan, tetapi file tidak ditemukan.")

        if not found_weak_creds and not wordlist_path:
            print(f"{C.MENU}  {SYM_FAILED} Semua kredensial default gagal untuk {service_name}.")


    print(f"{C.HEADER} ---------------------------------------------")

