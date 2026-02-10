# web_head.py
import requests

from app.utility.colors import C

REQUIRED_OPTIONS = {"URL": ""}


def execute(options):
    """Checking the security header of a URL."""

    target_url = options.get("URL")

    # 1. Make sure the URL has a scheme (http:// or https://)
    if not target_url.startswith(("https://", "http://")):
        target_url = "https://" + target_url

    print(f"{C.HEADER}\n CHECKING THE HEADER: {target_url}")

    try:

        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        response = requests.get(target_url, headers=headers, timeout=5)

        # 2. Iterate (Loop) through each Header received
        print(f"{C.MENU}\n  HEADER RECEIVED:")
        for header, value in response.headers.items():
            print(f"  {C.HEADER}{header}:{C.RESET} {value}")

        # 3. Security Validation
        print(f"{C.HEADER} \n--- HEADER SECURITY ANALYSIS ---\n")

        # Check the 'Server' Header (often exposed)
        server_header = response.headers.get("Server")
        if server_header:
            print(f"{C.ERROR}[!] Server Version Exposed: {server_header}{C.RESET}")
        else:
            print(f"{C.SUCCESS}[✓] Server header not found or hidden.{C.RESET}")

        # Check X-Frame-Options Security Header (Clickjacking Prevention)
        if "X-Frame-Options" not in response.headers:
            print(
                f"{C.ERROR}[!] X-Frame-Options header is MISSING. Potential for Clickjacking.{C.RESET}"
            )
        else:
            print(
                f"{C.SUCCESS}[✓] X-Frame-Options: {response.headers.get('X-Frame-Options')}. (Safe){C.RESET}"
            )

        # Strict-Transport-Security (Downgrade Prevention)
        if (
            "Strict-Transport-Security" not in response.headers
            and target_url.startswith("https://")
        ):
            print(
                f"{C.ERROR}[!] The Strict-Transport-Security header is MISSING. HTTP Downgrade Risks.{C.RESET}"
            )
        else:
            print(f"{C.SUCCESS}[✓] HSTS found.{C.RESET}")

        # 1. Check Content-Security-Policy (XSS Prevention)
        if "Content-Security-Policy" not in response.headers:
            print(
                f"{C.ERROR}[!] CSP Header MISSING. Risk of Cross-Site Scripting (XSS).{C.RESET}"
            )
        else:
            print(f"{C.SUCCESS}[✓] Content-Security-Policy found.{C.RESET}")

        # 2. Cek X-Content-Type-Options (Pencegahan MIME Sniffing)
        if response.headers.get("X-Content-Type-Options") != "nosniff":
            print(
                f"{C.ERROR}[!] X-Content-Type-Options is MISSING or misconfigured. Risk of MIME Sniffing.{C.RESET}"
            )
        else:
            print(f"{C.SUCCESS}[✓] X-Content-Type-Options: nosniff. (Safe){C.RESET}")

        # 3. Cek Referrer-Policy (Pencegahan Kebocoran Data URL)
        if "Referrer-Policy" not in response.headers:
            print(
                f"{C.ERROR}[!] Referrer-Policy header MISSING. Potential data leakage via Referrer header.{C.RESET}"
            )
        else:
            print(
                f"{C.SUCCESS}[✓] Referrer-Policy: {response.headers.get('Referrer-Policy')}.{C.RESET}"
            )

        set_cookie = response.headers.get("Set-Cookie")
        if set_cookie:
            if "HttpOnly" not in set_cookie:
                print(
                    f"{C.ERROR}[!] Cookie MISSING 'HttpOnly' flag. Vulnerable to XSS cookie theft.{C.RESET}"
                )
            if "Secure" not in set_cookie and target_url.startswith("https://"):
                print(
                    f"{C.ERROR}[!] Cookie MISSING 'Secure' flag. Can be captured via MITM.{C.RESET}"
                )
            if "SameSite" not in set_cookie:
                print(
                    f"{C.ERROR}[!] Cookie MISSING 'SameSite' flag. Potential CSRF risk.\n{C.RESET}"
                )

    except KeyboardInterrupt:
        return
    except requests.exceptions.RequestException as e:
        print(f"{C.ERROR}[x] ERROR WHILE CONNECTING TO {target_url}: {e}{C.RESET}\n")

    print(f"{C.HEADER} ---------------------------------------")
