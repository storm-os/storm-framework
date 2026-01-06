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
{C.MENU} Help command:
  help				: Displaying the manual
  show options			: View the variables that have been set (IP, PORT, ETC.)
  show modules			: Displaying module categories
  show <name_categories>	: Displays the complete contents
  search <filename>		: To search for files
  info				: Information Development
  back				: Back from current position
  exit				: Exit the application

{C.MENU} Command Workflow:
  use <nama_modul>		: Selecting a module
  set <key> <val>		: Filling in the parameters
  run / exploit			: Run the selected module
{C.HEADER}===============================================
    """)


# --- Cek update ---

# 1. Tentukan versi lokal tools saat ini
CURRENT_VERSION = "3.2.0"

def check_update():
    # URL mentah ke file version.txt di GitHub
    url = "https://raw.githubusercontent.com/Proot9/El-Cyber_Pentest/main/version.txt"
    try:
        response = requests.get(url, timeout=5)
        latest_version = response.text.strip()

        # Jika versi di GitHub lebih tinggi dari versi lokal
        if latest_version > CURRENT_VERSION:
            print(f"{C.HEADER}\n######################################")
            print(f"{C.SUCCESS}\n[!] Update available: v{latest_version} (Current version: v{CURRENT_VERSION})")
            print(f"{C.SUCCESS}\n[-] Type: pentest update")
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
    current_module_name = ""

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
                print(f"[-] Module '{module_name}' Not found.")

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
                        print(f"[-] File '{var_value}' not found!")
                else:
                    options[var_name] = var_value
                    print(f"{var_name} => {var_value}")
            else:
                print("[-] Use: set <NAMA_VARIABEL> <nilai>")

        # MENU SHOW
        elif cmd == "show":
            target_show = args[0].lower() if args else ""

            # 1. Menampilkan Kategori (show modules)
            if target_show == "modules":
                print(f"\n{C.HEADER}--- Categories ---")
                # List folder di dalam app/modules secara dinamis
                categories = [d for d in os.listdir("app/modules") if os.path.isdir(os.path.join("app/modules", d)) and d != "__pycache__"]
                for cat in categories:
                    print(f"  - {cat}")
                print(f"\n{C.INPUT}Use 'show <nama_kategori>' to see the contents.")

            # 2. Menampilkan Opsi (show options)
            elif target_show == "options":
                header_name = current_module_name if current_module else "GLOBAL"
                print(f"\n{C.HEADER}MODULE OPTIONS ({header_name}):")
                print(f"{'Name':<12} {'Current Setting':<25} {'Description'}")
                print(f"{'-'*12} {'-'*25} {'-'*15}")

                if current_module:
                    # Ambil REQUIRED_OPTIONS dari modul yang aktif
                    req = getattr(current_module, 'REQUIRED_OPTIONS', {})
                    for var_name, desc in req.items():
                        val = options.get(var_name, "unset")
                        print(f"{var_name:<12} {val:<25} {desc}")
                else:
                    # Tampilkan semua global options jika belum 'use' modul
                    for k, v in options.items():
                        val = v if v else "unset"
                        print(f"{k:<12} {val:<25} Global Variable")
                print("")

            # 3. Menampilkan Isi Kategori secara Dinamis (misal: show exploit)
            else:
                potential_path = os.path.join("app/modules", target_show)

                if os.path.isdir(potential_path) and target_show != "":
                    print(f"\n{C.HEADER}Modules in '{target_show}':")
                    print(f"{'-'*45}")
                    for root, dirs, files in os.walk(potential_path):
                        for file in files:
                            if file.endswith(".py") and file != "__init__.py":
                                # Menghasilkan path rapi (misal: scanner/portscan)
                                rel_path = os.path.relpath(os.path.join(root, file), "app/modules")
                                print(f"  - {rel_path.replace('.py', '')}")
                    print("")
                else:
                    print(f"{C.ERROR}[-] Not found 'show {target_show}'")

        # PERINTAH: searching modules
        elif cmd == "search":
            query = args[0].lower() if args else ""
            if not query:
                print("[-] Enter file name!")
                continue

            print(f"\n[*] Searching for file name: '{query}'")
            print(f"{'Module Path':<35} {'Category'}")
            print(f"{'-'*35} {'-'*15}")

            count = 0
            for root, dirs, files in os.walk("app/modules"):
                for file in files:
                    if file.endswith(".py") and file != "__init__.py":
                        # 1. Ambil nama file saja untuk difilter
                        file_name_only = file.replace(".py", "").lower()

                        # 2. Filter: Hanya jika kata kunci ada di NAMA FILE
                        if query in file_name_only:
                            count += 1
                            # 3. Ambil path lengkap (misal: exploit/firebase/db)
                            rel_path = os.path.relpath(os.path.join(root, file), "app/modules")
                            clean_path = rel_path.replace(".py", "")

                            # 4. Ambil kategori (nama folder paling atas)
                            category = rel_path.split(os.sep)[0]

                            # 5. Tampilkan sesuai ekspektasi kamu
                            print(f"{clean_path:<35} {category}")

            if count == 0:
                print(f"[-] '{query}' Not found.")
            else:
                print(f"\n[*] Found {count} module.")
            print("")

        # PERINTAH: Information Dev
        elif cmd == "info":
            if current_module:
                desc = getattr(current_module, 'DESCRIPTION', 'No description available.')
                auth = getattr(current_module, 'AUTHOR', 'Elzy')
                print(f"\n{C.HEADER}--- Module Information ---")
                print(f"Name   : {current_module_name}")
                print(f"Author : {auth}")
                print(f"Descr  : {desc}\n")

        # 5. PERINTAH: run / exploit
        elif cmd in ["run", "exploit"]:
            if not current_module:
                print(f"{C.ERROR}[!] No modules selected.")
                continue

            try:
                # Pastikan setiap file di modules punya fungsi bernama 'execute'
                current_module.execute(options)
            except AttributeError:
                print(f"[-] Error: Module {current_module_name} tidak punya fungsi 'execute(options)'")
            except Exception as e:
                print(f"[-] An error occurred during execution: {e}")

        elif cmd == "back":
            current_module = None

        elif cmd == "help":
            tampilkan_bantuan()

        elif cmd == "pentest update"
            run_update()

        elif cmd in ["exit"]:
            break

        else:
            print(f"[-] Command not recognized: {cmd}")

if __name__ == "__main__":
    main()
