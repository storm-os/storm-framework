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

    # ---------------------------------------------
    # 1. Open Port: Do Banner Grabbing
    # ---------------------------------------------
    try:
        result = s.connect_ex((target_ip, port))
        
        if result == 0:
            status_color = f"{C.SUCCESS} OPEN " + STATUS_OPEN
            banner_info = "No version information."

            try:
                # Especially for web services (HTTP/HTTPS), send a minimum request
                if port in [80, 443, 8080]:
                    # Send an HTTP HEAD request to trigger a Server Header response.
                    request = f"HEAD / HTTP/1.1\r\nHost: {target_ip}\r\n\r\n"
                    s.sendall(request.encode())

                # Accepts up to 1024 bytes of data (Banner Grabbing)
                banner = s.recv(1024)

                if banner:
                    banner_info = banner.decode(errors='ignore').strip()

                    # Banner Cleaning Logic
                    if port == 22:
                        # SSH: Take the first line only
                        banner_info = banner_info.split('\n')[0]
                    elif port in [80, 443, 8080]:
                        # HTTP: Try looking for the 'Server' header
                        server_header = next((line for line in banner_info.split('\n') if line.lower().startswith('server:')), None)
                        if server_header:
                            banner_info = server_header.strip()
                        else:
                            banner_info = "HTTP Response received."

            except socket.timeout:
                banner_info = "Timeout"
            except Exception as e:
                banner_info = f"ERROR: {e}"

            # Returns banner status and information
            return status_color, banner_info

    # ---------------------------------------------
    # 2. Closed Port
    # ---------------------------------------------
        else:
            s.close()
            return f"{C.ERROR} CLOSED " + STATUS_CLOSED, None

    except KeyboardInterrupt:
        raise KeyboardInterrupt
    finally:
        s.close()


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

    # Specify the total column width for the Port and Service Name sections.
    # Adjusted so that the colons are always aligned
    MAX_TOTAL_WIDTH = 30

    try:
        for port in ports_to_check:
            # Call the function that returns the status and banner
            status_line, banner = get_service_banner(target_ip, port)
            service_name = port_names.get(port, "Unknown Service")

            # 1. Setting up the initial part of the line (Port and Service Name)
 
            # The initial string to be aligned
            port_info_string = f"  Port {port} ({service_name})"

            # Calculating the required spacing (padding)
            # ljust() ensures the string has a MINIMUM width of 30 characters
            padding_string = port_info_string.ljust(MAX_TOTAL_WIDTH)

            # Creating initial output: Port 80 (HTTP): OPEN ✅
            output_line = f"{C.MENU}{padding_string}: {status_line}"

            # 2. Add Banner/Version (Only if port is open)
            if "OPEN" in status_line:
                if banner and "No information" not in banner and "Error while retrieving banner" not in banner:
                    clean_banner = banner.replace('\n', ' ').strip()
                    output_line += f" {C.MENU} | {C.SUCCESS}{clean_banner}"
                else:
                     # Info message if failed to retrieve banner
                     output_line += f" {C.MENU} | INFO: {banner}"

            # End the line with RESET
            output_line += f'{C.RESET}'

            # 3. Full Single Line Print
            print(output_line)
        print(f"{C.HEADER} --- SCAN COMPLETE ---\n")
     except KeyboardInterrupt:
        print(f"\n{C.ERROR}[!] Scan stopped.{C.RESET}")

