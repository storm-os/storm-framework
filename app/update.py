import os
import sys

def run_update():
    print(C["SUCCESS"] + "[+] Memulai pembaruan otomatis..." + C["RESET"])
    # Jalankan ulang install.sh
    update_command = "curl -fsSL https://raw.githubusercontent.com/Proot9/El-Cyber_Pentest/main/install.sh | bash"
    os.system(update_command)
    print(C["SUCCESS"] + "[+] Update selesai. Silakan jalankan kembali tools Anda." + C["RESET"])
    sys.exit()

