import subprocess
import os

REQUIRED_OPTIONS = {
    "INTERFACE": "example: eth0",
}


def execute(options):

    iface = options.get("INTERFACE")
    base_dir = os.path.dirname(os.path.abspath(__file__))
    bin_path = os.path.join(base_dir, "src", "dpi_netspy")

    if not os.path.isfile(bin_path):
        print(f"[!] ERROR: Binary not found {bin_path}.")
        return False

    print(f"[*] Run Go-Sniffer on interface: {iface}")

    try:
        # Calling a Go binary with interface arguments
        proc = subprocess.Popen(
            [bin_path, iface],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line.strip())

    except KeyboardInterrupt:
        print("\n[*] Stop Sniffer...")
        proc.terminate()
    except Exception as e:
        print(f"[!] ERROR: {e}")

    return True
