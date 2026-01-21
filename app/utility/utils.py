import os
import importlib
import textwrap

from app.utility.config_path import ROOT_DIR
from app.utility.colors import C
from lib.sqlite.helper_db import StormDatabase


"""
utils.py It all contains help logic to make it easier during repairs and updates.

This is included in the core category which cannot be modified.

"""
# LOGIC GLOBAL WORDLIST
def resolve_path(kata_kunci):
    if not kata_kunci: return None

    assets_dir = os.path.join(ROOT_DIR, "assets/wordlist")

    # Cek input manual dulu
    if os.path.exists(kata_kunci):
        return os.path.abspath(kata_kunci)

    # Cari di assets
    if os.path.exists(assets_dir):
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                if kata_kunci.lower() in file.lower():
                    return os.path.join(root, file)
    return None


# LOGIC SEARCHING
def load_module_dynamically(module_name):
    base_path = os.path.join(ROOT_DIR, "modules")

    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == f"{module_name}.py":
                # Ganti root_path menjadi ROOT_DIR di sini
                relative_path = os.path.relpath(os.path.join(root, file), ROOT_DIR)
                module_path = relative_path.replace(os.sep, ".").rstrip(".py")

                return importlib.import_module(module_path)
    return None



# UI MODULES
EXT = (".py", ".go", ".rs", ".c", ".cpp", ".rb", ".php",
       ".sh", ".js", ".ts", ".html"
)

def count_modules():
    total = 0
    # Ambil path absolut root
    path = os.path.join(ROOT_DIR, "modules")

    if not os.path.exists(path):
        return 0

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(EXT) and file != "__init__.py":
                total += 1
    return total


def count_by_category():
    """
    Menghitung jumlah modul berdasarkan folder kategori
    """
    stats = {}
    modules_path = os.path.join(ROOT_DIR, "modules")

    if not os.path.exists(modules_path):
        return stats

    # Ambil folder langsung di bawah /modules (sebagai kategori utama)
    categories = [d for d in os.listdir(modules_path)
                  if os.path.isdir(os.path.join(modules_path, d))]

    for cat in categories:
        cat_full_path = os.path.join(modules_path, cat)
        count = 0
        # Hitung file di dalam folder kategori tersebut (rekursif)
        for root, dirs, files in os.walk(cat_full_path):
            for file in files:
                if file.endswith(EXT) and file != "__init__.py":
                    count += 1

        # Masukkan ke dictionary jika folder tersebut berisi modul
        if count > 0:
            stats[cat] = count

    return stats



# LOGIC SHOW
def get_categories():
    """Mengambil daftar folder kategori di dalam /modules"""
    modules_path = os.path.join(ROOT_DIR, "modules")
    if not os.path.exists(modules_path):
        return []
    return [d for d in os.listdir(modules_path)
            if os.path.isdir(os.path.join(modules_path, d)) and d != "__pycache__"]

def get_modules_in_category(category):
    """Mengambil semua file .py di dalam kategori tertentu"""
    category_path = os.path.join(ROOT_DIR, "modules", category)
    modules_list = []

    if os.path.isdir(category_path):
        for root, dirs, files in os.walk(category_path):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    # Ambil path relatif terhadap folder modules root
                    rel_path = os.path.relpath(os.path.join(root, file), os.path.join(ROOT_DIR, "modules"))
                    modules_list.append(rel_path.replace('.py', ''))
    return modules_list


# LOGIC SHOW DB
def cve_summary():
    db = StormDatabase()
    cursor = db.conn.cursor()
    # Ambil data: ID (untuk nomor), CVE_ID, dan Title
    cursor.execute("SELECT id, cve_id, title FROM cve_library ORDER BY id ASC")
    rows = cursor.fetchall()

    if not rows:
        print(f"{C.ERROR}[!] Gudang CVE masih kosong.")
        return

    print(f"\n{C.SUCCESS}--- STORM-OS CVE CATALOG ({len(rows)} Data) ---{C.RESET}")
    print(f"{'No':<4} | {'CVE ID':<18} | {'Vulnerability Name'}")
    print("-" * 60)

    for row in rows:
        # row[0]=id, row[1]=cve_id, row[2]=title
        print(f"{row[0]:<4} | {row[1]:<18} | {row[2][:50]}...")



def detail_cve(target_cve):
    db = StormDatabase()
    cursor = db.conn.cursor()
    # Kita panggil datanya
    cursor.execute("SELECT * FROM cve_library WHERE cve_id = ?", (target_cve,))
    data = cursor.fetchone()

    if data:
        # Mapping sesuai PRAGMA table_info:
        # 0:id, 1:cve_id, 2:title, 3:description, 4:remediation,
        # 5:severity, 6:url, 7:scanner, 8:added_at

        cve_id      = data[1]
        title       = data[2]
        description = data[3]
        remediation = data[4]
        severity    = data[5]
        url         = data[6]
        scanner     = data[7]

        print(f"\n{C.HEADER}STORM-OS VULNERABILITY REPORT{C.RESET}")
        print("="*65)

        print(f"{C.SUCCESS}CVE ID      :{C.RESET} {cve_id}")
        print(f"{C.SUCCESS}NAME        :{C.RESET} {title}")
        print(f"{C.SUCCESS}SEVERITY    :{C.RESET} {severity}")
        print("-" * 65)

        # Gunakan textwrap agar description (indeks 3) tidak hancur
        print(f"{C.SUCCESS}DESCRIPTION:{C.RESET}")
        wrapper = textwrap.TextWrapper(width=60, initial_indent="  ", subsequent_indent="  ")
        # Bersihkan karakter aneh agar wrapping mulus
        clean_desc = str(description).replace("\n", " ").replace("  ", " ")
        for line in wrapper.wrap(clean_desc):
            print(line)

        print("-" * 65)

        print(f"{C.SUCCESS}REMEDIATION :{C.RESET} {remediation}")
        print(f"{C.SUCCESS}URL SOURCES :{C.RESET} {url}")
        print(f"{C.SUCCESS}SCANNER     :{C.RESET} {C.INPUT}{scanner}{C.RESET}")
        print("="*65 + "\n")
