import subprocess
import os
import sys

from app.utility.colors import C


def run_verif():
    bin_p = "app/base/check"

    if not os.path.exists(bin_p):
        print(f"[-] ERROR: Rust binary not found in {bin_p}")
        return False

    print(f"[*] [INTEGRITY] Launching Rust Engine")

    try:
        # Menjalankan Rust binary
        subprocess.run([bin_p])
    except Exception as e:
        print(f"[-] ERROR: {e}")

    return True


def check_critical_files():
    if not os.path.exists(".env"):
        print(f"{C.ERROR}[!] FATAL ERROR: Integrity Key (.env) is missing!{C.RESET}")
        print(
            f"[*] Storm cannot verify the database signature without your unique keys."
        )
        print(
            f"[*] Please run the installation/recovery script to regenerate your keys."
        )
        sys.exit(1)
