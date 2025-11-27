# dns.py

import dns.resolver
import socket
# Import time untuk potensi timeout yang lebih lama jika diperlukan

# Definisikan simbol status
SYM_INFO = "💡"
SYM_ERROR = "❌"
SYM_SECURITY = "🔒"

# List tipe record DNS yang ingin kita cari
DNS_RECORDS = ['A', 'MX', 'NS', 'TXT', 'AAAA', 'SOA']

def enumerate_dns_records(target_domain, C):
    """Mengambil berbagai tipe record DNS dari sebuah domain."""

    # Custom NameServer
    custom_resolver = dns.resolver.Resolver(configure=False)
    custom_resolver.nameservers = ['8.8.8.8', '1.1.1.1']

    dns.resolver.get_default_resolver = lambda: custom_resolver
    # ---------------------------------

    # 1. Pastikan target adalah domain yang valid, bukan IP Address
    if target_domain.replace('.', '').isdigit():
        print(C["ERROR"] + f"{SYM_ERROR} Error: Masukkan DOMAIN (ex: google.com), bukan IP Address.")
        print(C["HEADER"] + "---------------------------------------------")
        return

    print(C["HEADER"] + f"\n--- DNS ENUMERATION untuk {target_domain} ---")

    try:
        # 1. Pastikan domain bisa di-resolve ke IP (valid) - Cek awal
        try:
            socket.gethostbyname(target_domain)
        except socket.error:
            print(C["ERROR"] + f"{SYM_ERROR} Error: Domain tidak dapat di-resolve (mungkin tidak ada/offline).")
            print(C["HEADER"] + "---------------------------------------------")
            return

        # 2. Iterasi melalui setiap tipe record yang diinginkan
        for record_type in DNS_RECORDS:
            try:
                # Menggunakan resolver untuk query record
                # Set timeout (opsional, tapi baik untuk koneksi lambat)
                answers = custom_resolver.resolve(target_domain, record_type, lifetime=3.0)

                print(C["MENU"] + f"\n[{record_type} Records]:")

                for rdata in answers:
                    output_line = str(rdata)

                    # Beri penekanan khusus pada record keamanan (TXT)
                    if record_type == 'TXT':
                        print(C["SUCCESS"] + f"  {SYM_SECURITY} {output_line}" + C["RESET"])
                    else:
                        # Gunakan warna MENU untuk output reguler
                        print(C["MENU"] + f"  {SYM_INFO} {output_line}" + C["RESET"])

            except dns.resolver.NoAnswer:
                # Tidak ada record tipe ini (normal)
                pass
            except dns.resolver.NXDOMAIN:
                # Domain tidak ada (sudah dicek di awal, tapi jaga-jaga)
                pass
            except dns.resolver.Timeout:
                 print(C["ERROR"] + f"  {SYM_ERROR} Timeout saat mencoba mengambil {record_type} Records.")
                 # Jangan break loop, coba record_type berikutnya
            except Exception as e:
                # Kesalahan tak terduga (misalnya koneksi terputus)
                print(C["ERROR"] + f"  {SYM_ERROR} Error tak terduga pada {record_type}: {e}")

    except Exception as e:
        print(C["ERROR"] + f"{SYM_ERROR} Terjadi error umum: {e}")

    print(C["HEADER"] + "---------------------------------------------")
