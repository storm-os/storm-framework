# dns.py

import dns.resolver
import socket

from app.utility.colors import C

# Definisikan simbol status
SYM_INFO = "💡"
SYM_ERROR = "❌"
SYM_SECURITY = "🔒"

# List tipe record DNS yang ingin kita cari
DNS_RECORDS = ['A', 'MX', 'NS', 'TXT', 'AAAA', 'SOA']

REQUIRED_OPTIONS = {
        "URL"           : ""
    }

def execute(options):
    """Mengambil berbagai tipe record DNS dari sebuah domain."""

    target_domain = options.get("URL")

    # Custom NameServer
    custom_resolver = dns.resolver.Resolver(configure=False)
    custom_resolver.nameservers = ['8.8.8.8', '1.1.1.1']

    dns.resolver.get_default_resolver = lambda: custom_resolver
    # ---------------------------------

    # 1. Pastikan target adalah domain yang valid, bukan IP Address
    if target_domain.replace('.', '').isdigit():
        print(f"{C.ERROR} {SYM_ERROR} Error: Masukkan DOMAIN (ex: google.com), bukan IP Address.")
        print(f"{C.HEADER} ---------------------------------------------")
        return

    print(f"{C.HEADER} \n--- DNS ENUMERATION untuk {target_domain} ---")

    try:
        # 1. Pastikan domain bisa di-resolve ke IP (valid) - Cek awal
        try:
            socket.gethostbyname(target_domain)
        except socket.error:
            print(f"{C.ERROR} {SYM_ERROR} Error: Domain tidak dapat di-resolve (mungkin tidak ada/offline).")
            print(f"{C.HEADER} ---------------------------------------------")
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
                # Tidak ada record tipe ini (normal)
                pass
            except dns.resolver.NXDOMAIN:
                # Domain tidak ada (sudah dicek di awal, tapi jaga-jaga)
                pass
            except dns.resolver.Timeout:
                 print(f"{C.ERROR}  {SYM_ERROR} Timeout saat mencoba mengambil {record_type} Records.")
                 # Jangan break loop, coba record_type berikutnya
            except Exception as e:
                # Kesalahan tak terduga (misalnya koneksi terputus)
                print(f"{C.ERROR}  {SYM_ERROR} Error tak terduga pada {record_type}: {e}")

    except Exception as e:
        print(f"{C.ERROR} {SYM_ERROR} Terjadi error umum: {e}")

    print(f"{C.HEADER} ---------------------------------------------")
