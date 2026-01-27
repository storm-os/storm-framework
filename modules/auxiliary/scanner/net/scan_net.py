# scanner.py
import socket

from app.utility.colors import C

STATUS_OPEN = "✅"
STATUS_CLOSED = "❌"

def get_service_banner(target_ip, port, timeout=1.0):
    """
    Checking port status and trying to get banner/version information.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)

    result = s.connect_ex((target_ip, port))

    # ---------------------------------------------
    # 1. Port Terbuka: Lakukan Banner Grabbing
    # ---------------------------------------------
    if result == 0:
        status_color = f"{C.SUCCESS} OPEN " + STATUS_OPEN
        banner_info = "No version information."

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
                        banner_info = "HTTP Response received."

        except KeyboardInterrupt:
            return
        except socket.timeout:
            banner_info = f"Timeout"
        except Exception as e:
            banner_info = f"ERROR: {e}"

        finally:
            s.close()

        # Mengembalikan status dan informasi banner
        return status_color, banner_info

    # ---------------------------------------------
    # 2. Port Tertutup
    # ---------------------------------------------
    else:
        s.close()
        return f"{C.ERROR} CLOSED " + STATUS_CLOSED, None


REQUIRED_OPTIONS = {
        "IP"            : ""
    }

def execute(options):
    """The main function is to run a scan with version/banner detection.."""

    target_ip = options.get("IP")

    port_names = {
        # === Remote & legacy ===
        21: "FTP",
        22: "SSH",
        23: "Telnet",
        25: "SMTP",
        110: "POP3",
        143: "IMAP",

        # === DNS & Network ===
        53: "DNS",
        67: "DHCP",
        68: "DHCP",
        123: "NTP",
        161: "SNMP",
        389: "LDAP",

        # === Web standard ===
        80: "HTTP",
        443: "HTTPS",
        3000: "NodeJS",
        5000: "Flask",
        5173: "Vite Dev",
        8000: "Django",
        8008: "HTTP Alt",
        8080: "HTTP Alt Proxy",
        8443: "HTTPS Alt",
        8888: "Dev Panel",

        # === Admin / panel vibes (🔥 sering juicy) ===
        81: "HTTP Alt",
        2082: "cPanel",
        2083: "cPanel SSL",
        2086: "WHM",
        2087: "WHM SSL",
        2095: "Webmail",
        2096: "Webmail SSL",

        # === Database ===
        1433: "MSSQL",
        1521: "Oracle",
        3306: "MySQL",
        5432: "PostgreSQL",
        6379: "Redis",
        27017: "MongoDB",

        # === File & storage ===
        139: "NetBIOS",
        445: "SMB",
        2049: "NFS",

        # === Java / Enterprise ===
        7001: "WebL",
        7002: "WebL SSL",
        8081: "HTTP Alt",
        9000: "PHP-FPM",
        9043: "WebSphere",

        # === Containers / DevOps ===
        2375: "Docker API",
        2376: "Docker API SSL",
        6443: "Kubernetes API",

        # === Monitoring ===
        9090: "Prometheus",
        9091: "Supervisor",
        9200: "Elasticsearch",
        5601: "Kibana"
    }
    ports_to_check = port_names.keys()

    print(f"{C.HEADER}\n SCANNING: PORT & VERSION in {target_ip}")

    # Tentukan lebar kolom total untuk bagian Port dan Nama Layanan
    # Disesuaikan agar titik dua selalu sejajar
    MAX_TOTAL_WIDTH = 30

    for port in ports_to_check:
        # Panggil fungsi yang mengembalikan status dan banner
        status_line, banner = get_service_banner(target_ip, port)
        service_name = port_names.get(port, "Unknown Service")

        # 1. Menyiapkan bagian awal baris (Port dan Nama Layanan)

        # String awal yang akan disejajarkan
        port_info_string = f"  Port {port} ({service_name})"

        # Menghitung spasi yang diperlukan (padding)
        # ljust() memastikan string memiliki lebar MINIMUM 25 karakter
        padding_string = port_info_string.ljust(MAX_TOTAL_WIDTH)

        # Membuat output awal: Port 80 (HTTP)       : OPEN ✅
        # Kunci: Hapus \t dan gunakan ljust() untuk perataan konsisten
        output_line = f"{C.MENU}{padding_string}: {status_line}"

        # 2. Menambahkan Banner/Versi (Hanya jika port terbuka)
        if "OPEN" in status_line:

            if banner and "No information" not in banner and "Error while retrieving banner" not in banner:

                clean_banner = banner.replace('\n', ' ').strip()

                # Menambahkan pemisah dan Versi/Banner, konsisten dengan titik dua di Versi/Banner
                output_line += f" {C.MENU} | {C.SUCCESS}{clean_banner}"

            else:
                 # Pesan info jika gagal mengambil banner
                 output_line += f" {C.MENU} | INFO: {banner}"

        # Akhiri baris dengan RESET
        output_line += f'{C.RESET}'

        # 3. Cetak Baris Tunggal Penuh
        print(output_line)

    print(f"{C.HEADER} \n--- SCAN COMPLETE ---")
