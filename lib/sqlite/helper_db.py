import sqlite3
from pathlib import Path

# Ini cara paling cerdas karena dia deteksi otomatis lokasi file storage.py kamu
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "storage"
DB_DIR.mkdir(exist_ok=True)

class StormDatabase:
    def __init__(self, db_name="storm.db"):
        # Gunakan DB_DIR yang sudah dibuat di atas
        self.db_path = DB_DIR / db_name

        # Connect langsung pakai self.db_path
        self.conn = sqlite3.connect(str(self.db_path), check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # 1. Tabel Gudang CVE (Hasil Crawling info)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cve_library (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cve_id TEXT UNIQUE,
                title TEXT,
                description TEXT,
                remediation TEXT,
                severity TEXT,
                url TEXT,
                scanner TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. Tabel Gudang Target (Hasil Crawling Website)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS targets_pool (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                address TEXT UNIQUE,
                port INTEGER,
                service_name TEXT,
                is_vulnerable BOOLEAN DEFAULT 0,
                detected_cve TEXT,
                last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def add_target(self, address, port, service):
        """Fungsi untuk crawler memasukkan hasil temuan"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT OR IGNORE INTO targets_pool (address, port, service_name) VALUES (?, ?, ?)", 
                           (address, port, service))
            self.conn.commit()
        except Exception as e:
            print(f"[-] Database Error: {e}")

    def fetch_all_targets(self):
        """Mengambil semua daftar target dari gudang"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT address, port, service_name, is_vulnerable FROM targets_pool")
        return cursor.fetchall()

    def fetch_all_cve(self):
        """Mengambil info CVE untuk katalog (Ringkas)"""
        cursor = self.conn.cursor()
        # Tambahkan 'id' untuk penomoran di tabel katalog
        cursor.execute("SELECT id, cve_id, title, severity FROM cve_library ORDER BY id ASC")
        return cursor.fetchall()

    def fetch_cve_detail(self, cve_id):
        """Mengambil data lengkap satu CVE berdasarkan ID-nya"""
        cursor = self.conn.cursor()
        # Menggunakan parameter ? untuk keamanan (SQL Injection protection)
        cursor.execute("SELECT * FROM cve_library WHERE cve_id = ?", (cve_id,))
        return cursor.fetchone() # Pakai fetchone karena kita cuma mau ambil 1 data
