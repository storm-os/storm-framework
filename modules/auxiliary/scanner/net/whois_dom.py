# whois.py
import whois
from app.utility.colors import C


REQUIRED_OPTIONS = {
        "DOMAIN": "opsional",
}
def get_clean_data(data):
    """Tidy up the output which can be a list or None"""
    if isinstance(data, list):
        return ", ".join([str(i) for i in data if i])
    return data if data else "N/A"

def execute(options):
    target = options.get("DOMAIN")
    if not target:
        print(f"{C.ERROR} Error: Masukkan domain target!")
        return

    # Pembersihan URL
    clean_domain = target.replace('http://', '').replace('https://', '').split('/')[0].strip()

    print(f"{C.HEADER}\n[ DOMAIN WHOIS LOOKUP ] -> {clean_domain}")

    try:
        w = whois.whois(clean_domain)
        
        # Tampilkan Informasi
        print(f"{C.MENU} Registrar:      {C.RESET}{w.registrar}")
        print(f"{C.MENU} Created Date:   {C.RESET}{get_clean_data(w.creation_date)}")
        print(f"{C.MENU} Expiry Date:    {C.RESET}{get_clean_data(w.expiration_date)}")
        print(f"{C.MENU} Org:            {C.RESET}{w.org}")
        print(f"{C.MENU} Emails:         {C.RESET}{get_clean_data(w.emails)}")
        print(f"{C.MENU} Name Servers:   {C.RESET}{get_clean_data(w.name_servers)}")

    except Exception as e:
        print(f"{C.ERROR} ERROR: Unable to retrieve domain data.")
        print(f"{C.ERROR} Detail: {e}")
