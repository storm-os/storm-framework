import os
import sys

from app.utility.colors import C

def run_update():
    os.chdir(os.path.expanduser("~"))
    update_command = "curl -fsSL https://raw.githubusercontent.com/storm-os/Cyber-Pentest/main/install | bash "
    os.system(update_command)
    sys.exit()

