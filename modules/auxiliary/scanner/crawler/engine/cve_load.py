import subprocess
import json
from lib.sqlite.helper_db import StormDatabase
from app.utility.colors import C

REQUIRED_OPTIONS = {
        "COUNT"        : ""
}

def execute(options):

    count = options.get("COUNT")

    db = StormDatabase()
    print(f"{C.INFO}[*] Meminta Go-Engine mengambil {count} CVE...")

    try:
        # Kirim angka 'count' sebagai argumen ke binary Go
        process = subprocess.run(
            ['./script/crawler/cve_engine', str(count)],
            capture_output=True,
            text=True
        )

        if process.stdout:
            cve_list = json.loads(process.stdout)

            cursor = db.conn.cursor()
            for data in cve_list:
                cursor.execute('''
                    INSERT OR IGNORE INTO cve_library (
                        cve_id, title, severity, description, remediation, url, scanner
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['cve'], data['name'], data['severity'],
                    data['description'], json.dumps(data['remediation']),
                    json.dumps(data['URL']), data['scanner']
                ))

            db.conn.commit()
            print(f"{C.SUCCESS}[+] Berhasil menarik {len(cve_list)} data ke gudang!")

    except Exception as e:
        print(f"{C.ERROR}[-] Gagal sinkronisasi dengan Go-Engine: {e}")
