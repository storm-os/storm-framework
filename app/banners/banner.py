import os
import random
import importlib
from app.utility.colors import C
from app.utility.config_path import ROOT_DIR

def get_random_banner():
    # Gunakan ROOT_DIR agar lebih bersih
    banner_dir = os.path.join(ROOT_DIR, "lib", "ui", "banners")

    try:
        if not os.path.exists(banner_dir):
            return f"{C.SUCCESS}Cyber-Pentest Framework (Folder Not Found)"

        all_files = [f for f in os.listdir(banner_dir) if f.endswith(".py") and f != "__init__.py"]

        if not all_files:
            return f"{C.SUCCESS}Cyber-Pentest Framework"

        random_file = random.choice(all_files)
        module_path = f"lib.ui.banners.{random_file.replace('.py', '')}"

        # Reload module jika perlu atau import biasa
        banner_module = importlib.import_module(module_path)
        raw_banner = getattr(banner_module, 'DATA', 'Banner data not found.')

        # --- LOGIKA PENGUKUR LAYAR (RESPONSIVE) ---
        try:
            columns = os.get_terminal_size().columns
        except:
            columns = 80

        lines = raw_banner.splitlines()
        if not lines: return raw_banner

        # Cari baris terpanjang untuk menentukan lebar asli banner
        max_banner_width = max(len(line) for line in lines)

        # Hitung jarak spasi dari kiri agar pas di tengah
        padding_size = max(0, (columns - max_banner_width) // 2)
        padding_str = " " * padding_size

        # Gabungkan kembali dengan spasi tambahan di setiap baris
        centered_banner = "\n".join([f"{padding_str}{line}" for line in lines])

        return centered_banner

    except Exception as e:
        return f"Error loading banner: {e}"
