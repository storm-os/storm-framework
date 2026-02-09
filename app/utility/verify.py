import subprocess
import os


def execute(options):
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


