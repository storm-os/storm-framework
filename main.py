# main.py
# All import
import os
import requests
import readline
import textwrap

import app.base.config_ui as config_ui
import app.utility.utils as utils
import versi as v

from app.base.config_update import check_update
from app.utility.update import run_update
from app.utility.colors import C
from app.utility.search import search_modules
from app.banners.banner import get_random_banner

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



# --- Fungsi Menu ---

def main():
    clear_screen()
    print(get_random_banner())

    total = utils.count_modules()
    stats = utils.count_by_category()
    clean_stats = " | ".join([f"{cat.upper()}: {val}" for cat, val in stats.items()])
    full_text = f"[!] MODULE: {total} | {clean_stats}"
    wrapped_text = textwrap.fill(full_text, width=50, subsequent_indent="        ")
    print(f"{C.HEADER}\n+-- --=[ {C.INPUT}{wrapped_text} {C.HEADER}]=--")
    print("")
    print("The Cyber Pentest is a Proot9 Open Source Project")
    print(f"Run {C.SUCCESS}about{C.RESET} to view dev information.")
    print("")
    check_update()

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
        "USERNAME": "",
        "ID": "",
        "COUNT": "",
        "PATH": ""
    }

    while True:
        p_mod = f"({C.ERROR}{current_module_name}{C.INPUT})" if current_module else ""
        cmd_line = input(f"{C.INPUT}[~]{p_mod}==> ").strip().split()

        if not cmd_line: continue

        cmd = cmd_line[0].lower()
        args = cmd_line[1:]

        # 1. PERINTAH: use <module>
        if cmd == "use":
            module_name = args[0].lower() if args else ""
            mod = utils.load_module_dynamically(module_name) # Panggil fungsi dari utils
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
                    found_path = utils.resolve_path(var_value)
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
                categories = utils.get_categories()
                print(f"\n{C.HEADER}--- Categories ---")
                for cat in categories:
                    print(f"  - {cat}")
                print(f"\n{C.INPUT}Use 'show <category_name>' to see modules.")

            # 2. Menampilkan Opsi (show options)
            elif target_show == "options":
                header_name = current_module_name if current_module else "GLOBAL"
                print(f"\n{C.HEADER}MODULE OPTIONS ({header_name}):")
                print(f"{'Name':<12} {'Current Setting':<25} {'Description'}")
                print(f"{'-'*12} {'-'*25} {'-'*15}")

                if current_module:
                    req = getattr(current_module, 'REQUIRED_OPTIONS', {})
                    for var_name, desc in req.items():
                        val = options.get(var_name, "unset")
                        print(f"{var_name:<12} {val:<25} {desc}")
                else:
                    for k, v in options.items():
                        val = v if v else "unset"
                        print(f"{k:<12} {val:<25} Global Variable")

            # 3. Menampilkan Isi Kategori (misal: show exploit)
            else:
                module_files = utils.get_modules_in_category(target_show)
                if module_files:
                    print(f"\n{C.HEADER}Modules in '{target_show}':")
                    print(f"{'-'*45}")
                    for mod in module_files:
                        print(f"  - {mod}")
                    print("")
                else:
                    print(f"{C.ERROR}[-] Category or option '{target_show}' not found.")


        # PERINTAH: searching modules
        elif cmd == "search":
            query = args[0] if args else ""
            if not query:
                print("[-] Enter file name!")
                continue

            search_modules(query)

        # 5. PERINTAH: run / exploit
        elif cmd in ["run", "exploit"]:
            if not current_module:
                print(f"{C.ERROR}[!] No modules selected.")
                continue

            # --- VALIDASI ---
            valid_vars = getattr(current_module, 'REQUIRED_OPTIONS', {})
            missing_options = [key for key in valid_vars.keys() if not str(options.get(key, "")).strip()]

            if missing_options:
                print(f"{C.ERROR}[!] Failed to run. Variabel null.")
                print("")
                continue

            try:
                # Proses auto-path PASS
                user_pass_input = options.get("PASS")
                if user_pass_input:
                    full_path = utils.resolve_path(user_pass_input)
                    if full_path:
                        options["PASS"] = full_path

                # Eksekusi
                current_module.execute(options)

            except AttributeError:
                print(f"{C.ERROR}[-] Error: Module has no function 'execute(options)'")
            except Exception as e:
                print(f"{C.ERROR}[-] Error during execution: {e}")


        elif cmd == "back":
            current_module = None

        elif cmd == "help":
            config_ui.show_help()

        elif cmd == "about":
            config_ui.show_about()

        elif cmd == "update":
            run_update()

        elif cmd == "clear":
            clear_screen()
            print(get_random_banner())
            print(f"{C.HEADER}\n+-- --=[ {C.INPUT}{wrapped_text} {C.HEADER}]=--")
            print("")
            print("The Cyber Pentest is a Proot9 Open Source Project")
            print(f"Run {C.SUCCESS}about{C.RESET} to view dev information.")
            print("")

        elif cmd in ["exit"]:
            break

        else:
            print(f"[-] Unknown Command: {cmd}. Run the {C.SUCCESS}help{C.RESET} {C.INPUT}command for more details.")

if __name__ == "__main__":
    main()
