import os
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

    
    # 1. Determine Root with Precision
    base_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
    os.chdir(project_root)

    print(f"{C.SUCCESS}[*] Attempting to update Storm Framework.{C.RESET}")

    # 2. Check Connection & Fetch
    # Use rebase to be cleaner and not create messy merge commits.
    print(f"[*] Checking for new versions at github.com/storm-os/Cyber-Pentest")
    
    # We use subprocess to catch errors more elegantly.
    process = subprocess.run(["git", "pull", "--rebase", "origin", "main"], 
                             stdout=None,
                             stderr=subprocess.PIPE,
                             text=True
                            )
    # Live process
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        if "Already up to date" in process.stdout:
            print(f"{C.SUCCESS}[*] Storm-OS is already at the latest version.{C.RESET}")
        else:
            print(f"{C.SUCCESS}[+] Successfully pulled updates from remote.{C.RESET}")
            
            # 3. Trigger Compiler (The Hook)
            compiler_path = os.path.join(project_root, "compiler")
            if os.path.exists(compiler_path):
                print(f"{C.SUCCESS}[*] Triggering framework recompilation.{C.RESET}")
                os.system(f'bash -c "source {compiler_path} && compile_modules"')
                print(f"{C.SUCCESS}[✓] Framework updated to v{latest_version}{C.RESET}")
            else:
                print(f"{C.ERROR}[x] ERROR: Compiler hook not found at {compiler_path}{C.RESET}")
    else:
        print(f"{C.ERROR}[x] Update failed!{C.RESET}")
        print(f"{C.SUCCESS}[!] Logic: {process.stderr}{C.RESET}")
        print(f"[*] Suggestion: Run 'git stash' if you have local changes.")

    sys.exit()
