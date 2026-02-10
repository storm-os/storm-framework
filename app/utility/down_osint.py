import os
import subprocess
import sys


def install_osint_module():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "../../"))

    repo_url = "https://github.com/storm-os/OSINT.git"
    target_dir = os.path.join(project_root, "script", "osint")

    # 1. Clone/Update Repo
    if os.path.exists(os.path.join(target_dir, ".git")):
        print("[!] Module found. Updating...")
        subprocess.run(["git", "-C", target_dir, "pull"], check=True)
    else:
        print("[*] Downloading OSINT Module...")
        subprocess.run(["git", "clone", repo_url, target_dir], check=True)

    # 2. Instalasi via setup.py
    setup_file = os.path.join(target_dir, "setup.py")
    if os.path.exists(setup_file):
        print("[*] Detected setup.py. Installing module in editable mode...")
        # '-e .' artinya install folder ini sebagai package agar bisa di-import
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", target_dir], check=True
        )
        print("[✓] OSINT Package 'osint-storm' installed successfully.")

    try:
        from scripts.security.sign import generate_folder_manifest

        generate_folder_manifest()
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    install_osint_module()
