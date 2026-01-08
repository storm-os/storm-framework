import os
import sys

from app.utility.colors import C

def run_update():
    print(f"{C.SUCCESS} [+] Start automatic updates...")

    os.chdir(os.path.expanduser("~"))
    update_command = "curl -fsSL https://raw.githubusercontent.com/Proot9/Cyber-Pentest/main/install.sh | bash "
    os.system(update_command)

    print(f"{C.SUCCESS} [+] The update is complete. Please run your tools again.")
    sys.exit()

