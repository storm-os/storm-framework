import os
import sys
import requests
import subprocess

from app.utility.colors import C

def run_update():

    url = "https://raw.githubusercontent.com/storm-os/Cyber-Pentest/main/version.txt"
    try:
        response = requests.get(url, timeout=5)
        latest_version = response.text.strip()
    except:
        pass

    
    # 1. Tentukan Root dengan Presisi
    # Mengasumsikan storm.py ada di dalam subfolder, kita naik ke root
    base_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
    os.chdir(project_root)

    print(f"{C.SUCCESS}[*] Attempting to update Storm Framework.{C.RESET}")

    # 2. Cek Koneksi & Fetch (Cara MSF)
    # Menggunakan rebase agar lebih bersih dan tidak membuat commit merge yang berantakan
    print(f"[*] Checking for new versions at github.com/storm-os/Cyber-Pentest")
    
    # Kita gunakan subprocess agar bisa menangkap error dengan lebih elegan
    process = subprocess.run(["git", "pull", "--rebase", "origin", "main"], 
                             capture_output=True, text=True)

    if process.returncode == 0:
        if "Already up to date" in process.stdout:
            print(f"{C.SUCCESS}[*] Storm-OS is already at the latest version.{C.RESET}")
        else:
            print(f"{C.SUCCESS}[+] Successfully pulled updates from remote.{C.RESET}")
            
            # 3. Trigger Compiler (The Hook)
            compiler_path = os.path.join(project_root, "compiler")
            if os.path.exists(compiler_path):
                print(f"{C.SUCCESS}[*] Triggering framework recompilation.{C.RESET}")
                os.system(f'bash -c "source {compiler_path} && compile_modules"')
                print(f"{C.SUCCESS}[✓] Framework updated to v{latest_version}{C.RESET}")
            else:
                print(f"{C.ERROR}[x] ERROR: Compiler hook not found at {compiler_path}{C.RESET}")
    else:
        print(f"{C.ERROR}[x] Update failed!{C.RESET}")
        print(f"{C.SUCCESS}[!] Logic: {process.stderr}{C.RESET}")
        print(f"[*] Suggestion: Run 'git stash' if you have local changes.")

    sys.exit()
