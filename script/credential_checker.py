# credential_checker.py

import socket
import paramiko # Untuk SSH
import ftplib # Untuk FTP
import telnetlib # Untuk Telnet
import concurrent.futures

from script.wordlist import DEFAULT_CREDS

SYM_SUCCESS = "🔑"
SYM_FAILED = "🔒"
SYM_ERROR = "❌"

# --- Fungsi Pengujian SSH ---
def test_ssh(target_ip, port, username, password, C):
    """Mencoba login SSH menggunakan Paramiko."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(target_ip, port=port, username=username, password=password, timeout=2)
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
def test_ftp(target_ip, port, username, password, C):
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
def test_telnet(target_ip, port, username, password, C):
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

# --- Fungsi Utama ---
def check_default_credentials(target_ip, C):
    """Menjalankan pengujian kredensial lemah pada layanan umum."""

    print(C["HEADER"] + f"\n--- CREDENTIAL CHECKER untuk {target_ip} ---")

    # Port dan Protokol yang akan diuji
    services_to_test = {
        21: ("FTP", test_ftp),
        22: ("SSH", test_ssh),
        23: ("Telnet", test_telnet), # <-- test_telnet sudah didefinisikan
    }

    found_weak_creds = False

    for port, (service_name, test_function) in services_to_test.items():
        print(C["MENU"] + f"\n{service_name} (Port {port}) Analisis:")

        # Cek apakah port terbuka sebelum mencoba brute force
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        if s.connect_ex((target_ip, port)) != 0:
            print(C["ERROR"] + f"  {SYM_ERROR} Port {port} {service_name} tampaknya tertutup. Melewati.")
            s.close()
            continue
        s.close()

        # Mulai pengujian kredensial
        for user, passwd in DEFAULT_CREDS:
            if test_function(target_ip, port, user, passwd, C):
                print(C["SUCCESS"] + f"  {SYM_SUCCESS} LOGIN BERHASIL! ({service_name}) -> U:{user} P:{passwd}" + C["RESET"])
                found_weak_creds = True
                break # Berhenti setelah menemukan kredensial yang berhasil
            else:
                # Opsi: Menampilkan kredensial yang gagal
                print(C["MENU"] + f"  {SYM_FAILED} GAGAL: {user}:{passwd}")

        if not found_weak_creds:
            print(C["MENU"] + f"  {SYM_FAILED} Semua kredensial default gagal untuk {service_name}." + C["RESET"])

    print(C["HEADER"] + "---------------------------------------------")
