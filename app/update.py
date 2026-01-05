import os
import sys

from app.colors import C

def run_update():
    print(f"{C.SUCCESS} [+] Memulai pembaruan otomatis...")

    os.chdir(os.path.expanduser("~"))
    update_command = "curl -fsSL https://raw.githubusercontent.com/Proot9/El-Cyber_Pentest/main/install.sh | bash "
    os.system(update_command)

    print(f"{C.SUCCESS} [+] Update selesai. Silakan jalankan kembali tools Anda.")
    sys.exit()

