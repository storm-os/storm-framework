# scanner.py
import socket

STATUS_OPEN = "✅"
STATUS_CLOSED = "❌"

def quick_port_scan(target_ip, port, C):
    """Mengecek status satu port (Open/Closed)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)

    result = s.connect_ex((target_ip, port))
    s.close()

    if result == 0:
        # Panggil warna dari C dan tambahkan simbol
        return C["SUCCESS"] + "OPEN " + STATUS_OPEN
    else:
        # Panggil warna dari C dan tambahkan simbol
        return C["ERROR"] + "CLOSED " + STATUS_CLOSED

def scan_target(target_ip, C):
    """Fungsi utama untuk menjalankan scan pada port umum."""

    port_names = {
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        53: "DNS",
        161: "SNMP",
        80: "HTTP",
        443: "HTTPS",
        8080: "HTTP Alt",
        5000: "FLASK",
        8000: "Django"
    }
    ports_to_check = port_names.keys()

    # Menggunakan warna HEADER dari C
    print(C["HEADER"] + f"\n--- SCANNING PORTS di {target_ip} ---")

    for port in ports_to_check:
        status = quick_port_scan(target_ip, port, C)
        service_name = port_names.get(port, "Unknown Service")

        # Menggunakan warna MENU dari C untuk output utama
        print(C["MENU"] + f"  Port {port} ({service_name}):\t{status}")

    # Menggunakan warna HEADER dari C
    print(C["HEADER"] + "--- SCAN SELESAI ---")
