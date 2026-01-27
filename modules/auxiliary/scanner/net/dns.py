# dns.py

import dns.resolver
import dns.exception
import socket

from app.utility.colors import C

# Definisikan simbol status
SYM_INFO = "💡"
SYM_SECURITY = "🔒"

# List tipe record DNS yang ingin kita cari
DNS_RECORDS = [
    # === Core addressing ===
    'A',        # IPv4
    'AAAA',     # IPv6
    'CNAME',    # Alias / takeover risk 🔥

    # === Mail ===
    'MX',       # Mail server
    'TXT',      # SPF, DKIM, DMARC, verification

    # === Authority & zone ===
    'NS',       # Nameserver
    'SOA',      # Zone info (serial, refresh)

    # === Service discovery ===
    'SRV',      # _sip, _ldap, _xmpp, internal services 👀
    'NAPTR',    # VoIP / telecom (rare tapi kadang bocor info)

    # === Security / SSL ===
    'CAA',      # Allowed CA (fingerprinting infra)
    'TLSA',     # DANE (jarang tapi worth check)

    # === Reverse / legacy ===
    'PTR',

    # === DNSSEC (info only, bukan vuln langsung)
    'DNSKEY',
    'DS',
    'RRSIG',

    # === Microsoft / enterprise vibes ===
    'LOC'
]

REQUIRED_OPTIONS = {
        "DOMAIN"           : ""
    }

def execute(options):
    """Retrieving various types of DNS records from a domain."""

    target_domain = options.get("DOMAIN")

    # Custom NameServer
    custom_resolver = dns.resolver.Resolver(configure=False)
    custom_resolver.nameservers = ['8.8.8.8', '1.1.1.1']

    dns.resolver.get_default_resolver = lambda: custom_resolver
    # ---------------------------------

    # 1. Pastikan target adalah domain yang valid, bukan IP Address
    if target_domain.replace('.', '').isdigit():
        print(f"{C.ERROR}[!] ERROR: ENTER DOMAIN (ex: google.com).")
        print(f"{C.HEADER} ---------------------------------------------")
        return

    print(f"{C.HEADER}\n DNS ENUMERATION For {target_domain}\n")

    try:
        # 1. Pastikan domain bisa di-resolve ke IP (valid) - Cek awal
        try:
            socket.gethostbyname(target_domain)
        except socket.error:
            print(f"{C.ERROR}[!] ERROR: Domain cannot be resolved.")
            print(f"{C.HEADER} ---------------------------------------------\n")
            return

        # 2. Iterasi melalui setiap tipe record yang diinginkan
        for record_type in DNS_RECORDS:
            try:
                # Menggunakan resolver untuk query record
                # Set timeout (opsional, tapi baik untuk koneksi lambat)
                answers = custom_resolver.resolve(target_domain, record_type, lifetime=3.0)

                print(f"{C.MENU} \n[{record_type} Records]:")

                for rdata in answers:
                    output_line = str(rdata)

                    # Beri penekanan khusus pada record keamanan (TXT)
                    if record_type == 'TXT':
                        print(f"{C.SUCCESS}  {SYM_SECURITY} {output_line}")
                    else:
                        # Gunakan warna MENU untuk output reguler
                        print(f"{C.MENU}  {SYM_INFO} {output_line}")

            except dns.resolver.NoAnswer:
                pass
            except dns.resolver.NXDOMAIN:
                pass
            except dns.exception.Timeout:
                print(f"{C.ERROR}[!] Timeout {record_type} Records.\n")
                pass # Next
            except Exception as e:
                print(f"{C.ERROR}[!] ERROR {record_type}: {e}\n")
                continue


    except KeyboardInterrupt:
        return
    except Exception as e:
        print(f"{C.ERROR}[!] ERROR: {e}\n")

    print(f"{C.HEADER} ---------------------------------------------\n")
