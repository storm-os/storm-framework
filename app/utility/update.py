import sys
import re
import requests
import subprocess

from app.utility.colors import C


def run_update():

    url = "https://raw.githubusercontent.com/storm-os/storm-framework/main/version.txt"
    try:
        response = requests.get(url, timeout=5)
        latest_version = response.text.strip()
    except:
        pass

    print(f"{C.SUCCESS}[*] Attempting to update Storm Framework.{C.RESET}")

    pattern = re.compile(r"Receiving objects:.*,\s([\d\.]+ [KMGT]?i?B) \|")
    # 1. Get the latest info without changing the locale first
    process = subprocess.Popen(
        ["git", "fetch", "--all", "--progress"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    for line in process.stdout:
        match = pattern.search(line)
        if match:
            bytes_received = match.group(1)
            print(f"\rProgress update: {bytes_received}", end="")
            sys.stdout.flush()
    process.wait()

    # 2. CHECK CHANGES: Compare local (HEAD) with server (origin/main)
    check_diff = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "origin/main"],
        capture_output=True,
        text=True,
    )

    # 3. Reset Execution (Update file to the latest version)
    process = subprocess.run(
        ["git", "reset", "--hard", "origin/main"], stderr=subprocess.PIPE, text=True
    )

    if process.returncode == 0:
        print(f"{C.SUCCESS}\n[✓] System updated to version: {latest_version}{C.RESET}")

    # 4. Trigger Compiler ONLY IF needed
    try:
        from scripts.security.sign import generate_folder_manifest

        generate_folder_manifest()
    except Exception as e:
        print(f"ERROR: {e}")

    sys.exit()
