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
                             stderr=subprocess.PIPE,
                             text=True
                            )

    if process.returncode == 0:
        print(f"{C.SUCCESS}\n[+] Git synchronization complete.{C.RESET}")
            
        # 3. Trigger Compiler (The Hook)
        compiler_path = os.path.join(project_root, "compiler")
        if os.path.exists(compiler_path):
            print(f"{C.SUCCESS}\n[*] Triggering framework recompilation.{C.RESET}")
            os.system(f'bash -c "source {compiler_path} && compile_modules"')
            print(f"{C.SUCCESS}\n[✓] Framework updated to v{latest_version}{C.RESET}")
        else:
            print(f"{C.ERROR}\n[x] ERROR: Compiler hook not found at {compiler_path}{C.RESET}")
    else:
        print(f"{C.ERROR}\n[x] Update failed!{C.RESET}")
        print(f"{C.SUCCESS}[!] Logic: {process.stderr}{C.RESET}")
        print(f"[*] Suggestion: Run 'git stash' if you have local changes.")

    sys.exit()
