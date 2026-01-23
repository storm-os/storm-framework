import subprocess
import os

def execute(options):
    db = "tests/database/signed_manifest.json"
    bin_p = "modules/security/integrity/src/target/release/integrity"

    if not os.path.exists(bin_p):
        print(f"[-] ERROR: Rust binary not found in {bin_p}")
        return False

    if not os.path.exists(db):
        print(f"[-] ERROR: JSON manifest not found in {db}")
        return False

    print(f"[*] [INTEGRITY] Launching Rust Engine")
    print(f"[*] [SCANNING] Verifying signatures in {db}")

    try:
        # Menjalankan Rust binary
        subprocess.run([bin_p, db])
    except Exception as e:
        print(f"[-] ERROR: {e}")

    return True
