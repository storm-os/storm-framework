import os
import random
import importlib
from app.colors import C

def get_random_banner():
    # 1. Tentukan lokasi folder banners
    banner_dir = "app/lib/ui/banners"

    try:
        # 2. List semua file .py di folder tersebut (kecuali __init__.py)
        all_files = [f for f in os.listdir(banner_dir) if f.endswith(".py") and f != "__init__.py"]

        if not all_files:
            return f"{C.SUCCESS}El-Cyber Pentest Framework"

        # 3. Pilih satu file secara acak
        random_file = random.choice(all_files)

        # 4. Import file tersebut secara dinamis (tanpa .py)
        module_name = f"app.lib.ui.banners.{random_file.replace('.py', '')}"
        banner_module = importlib.import_module(module_name)

        # 5. Ambil variabel 'DATA' dari dalam file tersebut
        return getattr(banner_module, 'DATA', 'Banner data not found.')

    except Exception as e:
        return f"Error loading banner: {e}"
