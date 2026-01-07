import os
import importlib

def resolve_path(kata_kunci):
    if not kata_kunci: return None

    # DIAGNOSA DIMULAI
    current_file = os.path.abspath(__file__)
    app_folder = os.path.dirname(current_file)
    parent_folder = os.path.dirname(app_folder)
    assets_dir = os.path.join(parent_folder, "assets")

    if os.path.exists(assets_dir):
        # List file apa saja yang ada di sana untuk bukti
        files_in_assets = os.listdir(assets_dir)

    if os.path.exists(kata_kunci):
        return os.path.abspath(kata_kunci)

    if os.path.exists(assets_dir):
        for root, dirs, files in os.walk(assets_dir):
            for file in files:
                if kata_kunci.lower() in file.lower():
                    return os.path.join(root, file)
    return None


def load_module_dynamically(module_name):
    """
    Mencari file di dalam folder app/modules/ secara rekursif
    dan me-load fungsinya secara otomatis.
    """
    base_path = os.path.join(os.path.dirname(__file__), "modules")

    for root, dirs, files in os.walk(base_path):
        for file in files:
            # Cari file .py yang namanya cocok dengan module_name
            if file == f"{module_name}.py":
                # Ubah path file menjadi format import python (misal: app.modules.scanner.portscan)
                relative_path = os.path.relpath(os.path.join(root, file), os.path.dirname(os.path.dirname(__file__)))
                module_path = relative_path.replace(os.sep, ".").rstrip(".py")

                # Load modulnya
                return importlib.import_module(module_path)
    return None

def count_modules():
    total = 0
    # Tentukan path folder modules kamu
    path = "app/modules"

    if not os.path.exists(path):
        return 0

    for root, dirs, files in os.walk(path):
        for file in files:
            # Hanya hitung file .py dan abaikan __init__.py
            if file.endswith(".py") and file != "__init__.py":
                total += 1
    return total
