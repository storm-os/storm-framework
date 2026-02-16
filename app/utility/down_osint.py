import os
import subprocess
import sys
from rootmap import ROOT


def install_osint_module():
    repo_url = "https://github.com/storm-os/OSINT.git"
    target_dir = os.path.join(ROOT, "script", "osint")

    # 1. Clone Repo
    if os.path.exists(os.path.join(target_dir, ".git")):
        print("[!] Module found. Updating...")
        subprocess.run(["git", "-C", target_dir, "pull"], check=True)
    else:
        print("[*] Downloading OSINT Module...")
        subprocess.run(["git", "clone", repo_url, target_dir], check=True)

    # 2. Installation via setup.py
    setup_file = os.path.join(target_dir, "setup.py")
    if os.path.exists(setup_file):
        print("[*] Detected setup.py. Installing module in editable mode...")
        # '-e .' This means install this folder as a package so that it can be imported.
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", target_dir], check=True
        )
        print("[✓] OSINT Package 'osint-storm' installed successfully.")

    try:
        from scripts.security.sign import generate_folder_manifest
        import app.utility.load_var as ld

        generate_folder_manifest()
        ld.load_variable()
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    install_osint_module()
