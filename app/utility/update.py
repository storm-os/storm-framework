import sys
import requests
import subprocess

from app.utility.colors import C

def run_update():

    url = "https://raw.githubusercontent.com/storm-os/Cyber-Pentest/main/version.txt"
    try:
        response = requests.get(url, timeout=5)
        latest_version = response.text.strip()
    except:
        pass


    print(f"{C.SUCCESS}[*] Attempting to update Storm Framework.{C.RESET}")

    # 1. Get the latest info without changing the locale first
    subprocess.run(["git", "fetch", "--all"], stdout=subprocess.DEVNULL)

    # 2. CHECK CHANGES: Compare local (HEAD) with server (origin/main)
    check_diff = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "origin/main"],
        capture_output=True, text=True
    )

    # 3. Reset Execution (Update file to the latest version)
    process = subprocess.run(["git", "reset", "--hard", "origin/main"],
                             stderr=subprocess.PIPE, text=True)

    if process.returncode == 0:
        print(f"{C.SUCCESS}\n[+] System updated to latest version.{C.RESET}")

    # 4. Trigger Compiler ONLY IF needed
    try:
        from scripts.security.sign import generate_folder_manifest
        generate_folder_manifest()
    except Exception as e:
        print(f"ERROR: {e}")

    sys.exit()
