import os
import sys


def run_update():
    os.chdir(os.path.expanduser("~"))
    update_command = "curl -fsSL https://raw.githubusercontent.com/storm-os/Cyber-Pentest/main/setup | bash "
    os.system(update_command)
    sys.exit()

