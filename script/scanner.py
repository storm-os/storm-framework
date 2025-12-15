# scanner.py
import socket
import time

STATUS_OPEN = "✅"
STATUS_CLOSED = "❌"

def get_service_banner(target_ip, port, C, timeout=1.0):
    """
    Mengecek status port dan mencoba mendapatkan banner/informasi versi.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    result = s.connect_ex((target_ip, port))

    # ---------------------------------------------
    # 1. Port Terbuka: Lakukan Banner Grabbing
    # ---------------------------------------------
    if result == 0:
        status_color = C["SUCCESS"] + "OPEN " + STATUS_OPEN + C["RESET"]
        banner_info = "Tidak ada informasi versi."

        try:
            # Khusus untuk layanan web (HTTP/HTTPS), kirim request minimal
            if port in [80, 443, 8080]:
                # Kirim HTTP HEAD request untuk memicu respons Server Header
                request = f"HEAD / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
                s.sendall(request.encode())

            # Menerima hingga 1024 bytes data (Banner Grabbing)
            banner = s.recv(1024)

            if banner:
                banner_info = banner.decode(errors='ignore').strip()

                # Logika Pembersihan Banner
                if port == 22:
                    # SSH: Ambil baris pertama saja
                    banner_info = banner_info.split('\n')[0]
                elif port in [80, 443, 8080]:
                    # HTTP: Coba cari header 'Server'
                    server_header = next((line for line in banner_info.split('\n') if line.lower().startswith('server:')), None)
                    if server_header:
                        banner_info = server_header.strip()
                    else:
                        banner_info = "HTTP Response diterima."

        except socket.timeout:
            banner_info = "OPEN. Timeout."
        except Exception as e:
            banner_info = f"OPEN. Error."

        finally:
            s.close()

        # Mengembalikan status dan informasi banner
        return status_color, banner_info

    # ---------------------------------------------
    # 2. Port Tertutup
    # ---------------------------------------------
    else:
        s.close()
        return C["ERROR"] + "CLOSED " + STATUS_CLOSED + C["RESET"], None


def scan_target(target_ip, C):
    """Fungsi utama untuk menjalankan scan dengan deteksi versi/banner."""

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

    print(C["HEADER"] + f"\n--- SCANNING: PORT & VERSION di {target_ip} ---")

    # Tentukan lebar kolom total untuk bagian Port dan Nama Layanan
    # Disesuaikan agar titik dua selalu sejajar
    MAX_TOTAL_WIDTH = 25

    for port in ports_to_check:
        # Panggil fungsi yang mengembalikan status dan banner
        status_line, banner = get_service_banner(target_ip, port, C)
        service_name = port_names.get(port, "Unknown Service")

        # 1. Menyiapkan bagian awal baris (Port dan Nama Layanan)

        # String awal yang akan disejajarkan
        port_info_string = f"  Port {port} ({service_name})"

        # Menghitung spasi yang diperlukan (padding)
        # ljust() memastikan string memiliki lebar MINIMUM 25 karakter
        padding_string = port_info_string.ljust(MAX_TOTAL_WIDTH)

        # Membuat output awal: Port 80 (HTTP)       : OPEN ✅
        # Kunci: Hapus \t dan gunakan ljust() untuk perataan konsisten
        output_line = C["MENU"] + f"{padding_string}: {status_line}"

        # 2. Menambahkan Banner/Versi (Hanya jika port terbuka)
        if "OPEN" in status_line:

            if banner and "Tidak ada informasi" not in banner and "Error saat mengambil banner" not in banner:

                clean_banner = banner.replace('\n', ' ').strip()

                # Menambahkan pemisah dan Versi/Banner, konsisten dengan titik dua di Versi/Banner
                output_line += f" {C['MENU']} | {C['SUCCESS']}Versi: {clean_banner}"

            else:
                 # Pesan info jika gagal mengambil banner
                 output_line += f" {C['MENU']} | INFO: {banner}"

        # Akhiri baris dengan RESET
        output_line += C['RESET']

        # 3. Cetak Baris Tunggal Penuh
        print(output_line)

    print(C["HEADER"] + "--- SCAN SELESAI ---" + C["RESET"])
