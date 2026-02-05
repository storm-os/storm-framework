import os
import sys
import requests

from app.utility.colors import C

def run_update():

    url = "https://raw.githubusercontent.com/storm-os/Cyber-Pentest/main/version.txt"
    try:
        response = requests.get(url, timeout=5)
        latest_version = response.text.strip()
    except:
        pass
        
    print(f"{C.SUCCESS}[*] Storm-OS Update System{C.RESET}")
    
    # Masuk ke folder tempat script ini berada
    project_dir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(project_dir)

    print(f"{C.SUCCESS}[*] Synchronizing with GitHub.{C.RESET}")
    
    # Karena dijalankan dengan sudo, git pull & compiler pasti punya izin tulis
    # Kita gunakan --force untuk memastikan file lokal tertimpa jika ada konflik kecil
    update_exit_code = os.system("git fetch --all && git reset --hard origin/main")

    if update_exit_code == 0:
        if os.path.exists("./compiler"):
            print(f"{C.SUCCESS}[*] Changes detected. Re-compiling modules.{C.RESET}")
            # Langsung panggil compiler tanpa ragu
            os.system('bash -c "source ./compiler && compile_modules"')
            print(f"{C.SUCCESS}[✓] Cyber-Pentest v{latest_version} Updated Successfully!{C.RESET}")
        else:
            print(f"{C.ERROR}[x] ERROR: Compiler script missing!{C.RESET}")
    else:
        print(f"{C.ERROR}[x] Update failed: Check your internet connection.{C.RESET}")
    
    sys.exit()
