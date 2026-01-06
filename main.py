# main.py
import os
import requests
import readline

from app.update import run_update
from app.colors import C
from app.utils import resolve_path
from app.utils import load_module_dynamically

# --- Fungsi Clear Screen ---

def clear_screen():
    """Membersihkan layar terminal"""
    # Fungsi Win
    if os.name == 'nt':
       os.system('cls')
    # Fungsi Linux
    else:
       os.system('clear')

# --- Akhir fungsi clear screen ---

# --- MENU HELP
def tampilkan_bantuan():
    print(f"""
{C.HEADER}================ COMMAND GUIDE ================
{C.MENU} Perintah Umum:
  help			: Menampilkan panduan ini
  show options		: Melihat variabel yang sudah di-set (IP, Port, dll)
  back			: Keluar dari modul saat ini
  exit			: Keluar dari aplikasi

{C.MENU} Perintah Workflow:
  use <nama_modul>	: Memilih modul (Contoh: use scanner)
  set <key> <val>	: Mengisi parameter (Contoh: set target 192.168.1.1)
  run / exploit		: Menjalankan modul yang sudah dipilih
{C.HEADER}===============================================
    """)


# --- Cek update ---

# 1. Tentukan versi lokal tools saat ini
CURRENT_VERSION = "3.1.0"

def check_update():
    # URL mentah ke file version.txt di GitHub
    url = "https://raw.githubusercontent.com/Proot9/El-Cyber_Pentest/main/version.txt"
    try:
        response = requests.get(url, timeout=5)
        latest_version = response.text.strip()

        # Jika versi di GitHub lebih tinggi dari versi lokal
        if latest_version > CURRENT_VERSION:
            print(f"{C.HEADER}\n######################################")
            print(f"{C.SUCCESS}\n[!] Update tersedia: v{latest_version} (Versi Anda: v{CURRENT_VERSION})")
            print(f"{C.SUCCESS}\n[-] Ketik: npm update pentest")
            print(f"{C.HEADER}\n######################################")
    except:
        pass

# --- Akhir fungsi cek update ---

# --- Fungsi Menu ---

def banner():
    """Menampilkan pilihan menu utama dengan warna."""
    print(f"{C.HEADER}######################################")
    print(f"{C.HEADER}######################################")
    print(f"{C.HEADER}       Welcome to Cyber-Pentest  ")
    print(f"{C.HEADER}######################################")
    print(f"{C.HEADER}######################################")
    print(f"{C.HEADER} --------------------------------------")

def main():
    clear_screen()
    banner()
    current_module = None


    options = {
        "IP": "",
        "PORT": "",
        "PASS": "",
        "URL": "",
        "EMAIL": "",
        "HASH": "",
        "MESSAGE": "",
        "ID": "",
        "COUNT": "",
        "PATH": ""
    }

    while True:
        check_update()

        p_mod = f"({C.ERROR}{current_module_name}{C.INPUT})" if current_module else ""
        cmd_line = input(f"{C.INPUT}[~]{p_mod}==> ").strip().split()

        if not cmd_line: continue

        cmd = cmd_line[0].lower()
        args = cmd_line[1:]

        # 1. PERINTAH: use <module>
        if cmd == "use":
            module_name = args[0].lower() if args else ""
            mod = load_module_dynamically(module_name) # Panggil fungsi dari utils
            if mod:
                current_module = mod
                current_module_name = module_name
            else:
                print(f"[-] Modul '{module_name}' tidak ditemukan di folder modules/.")

        # 2. PERINTAH: set <VARIABLE> <VALUE>
        elif cmd == "set":
            if len(args) >= 2:
                var_name = args[0].upper()
                var_value = args[1]

                # Logika otomatis jika yang di-set adalah path file
                if "PATH" in var_name:
                    found_path = resolve_path(var_value)
                    if found_path:
                        options[var_name] = found_path
                        print(f"{var_name} => {found_path}")
                    else:
                        print(f"[-] File '{var_value}' tidak ditemukan!")
                else:
                    options[var_name] = var_value
                    print(f"{var_name} => {var_value}")
            else:
                print("[-] Gunakan: set <NAMA_VARIABEL> <nilai>")

        # 3. MENU HELP
        elif cmd == "help":
            tampilkan_bantuan()

        # 4. PERINTAH: show <options/modules>
        elif cmd == "show":
            target_show = args[0].lower() if args else ""
            if target_show == "options":
                print("\nGlobal Options:")
                for k, v in options.items():
                    print(f"  {k:<12} : {v}")
                print("")

        # 5. PERINTAH: run / exploit
        elif cmd in ["run", "exploit"]:
            if not current_module:
                print("[-]==>  ")
                continue

            try:
                # Pastikan setiap file di modules punya fungsi bernama 'execute'
                current_module.execute(options)
            except AttributeError:
                print(f"[-] Error: Modul {current_module_name} tidak punya fungsi 'execute(options)'")
            except Exception as e:
                print(f"[-] Terjadi kesalahan saat eksekusi: {e}")

        elif cmd == "back":
            current_module = None

        elif cmd in ["exit"]:
            break

        else:
            print(f"[-] Perintah tidak dikenal: {cmd}")

if __name__ == "__main__":
    main()
