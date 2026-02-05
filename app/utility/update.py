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

    
    # Determine Root with Precision
    base_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, "..", ".."))
    os.chdir(project_root)

    print(f"{C.SUCCESS}[*] Attempting to update Storm Framework.{C.RESET}")

    # 1. Get the latest info without changing the locale first
    subprocess.run(["git", "fetch", "--all"], stdout=subprocess.DEVNULL)
    
    # 2. CHECK CHANGES: Compare local (HEAD) with server (origin/main)
    # Check if there are any different .go or .c files
    check_diff = subprocess.run(
        ["git", "diff", "--name-only", "HEAD", "origin/main"],
        capture_output=True, text=True
    )
    
    # Filter: are there any files ending in .go or .c?
    changed_files = check_diff.stdout.splitlines()
    needs_recompile = any(f.endswith(('.go', '.c')) for f in changed_files)

    # 3. Reset Execution (Update file to the latest version)
    process = subprocess.run(["git", "reset", "--hard", "origin/main"], 
                             stderr=subprocess.PIPE, text=True)

    if process.returncode == 0:
        print(f"{C.SUCCESS}\n[+] System updated to latest version.{C.RESET}")
        
        # 4. Trigger Compiler ONLY IF needed
        compiler_path = os.path.join(project_root, "compiler")
        if needs_recompile:
            print(f"{C.SUCCESS}\n[*] Source code changes detected.{C.RESET}")
            os.system(f'bash -c "source {compiler_path} && compile_modules"')
            print(f"{C.SUCCESS}\n[✓] Framework recompiled successfully.{C.RESET}")    
        else:
            os.system(f'bash -c "source {compiler_path} && sign_binaries"')
            
        print(f"{C.SUCCESS}\n[✓] Storm is now v{latest_version}{C.RESET}")
        

    sys.exit()
