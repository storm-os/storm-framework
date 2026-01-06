import os
import importlib

def resolve_path(kata_kunci):
    """Mencari file di folder assets secara otomatis atau validasi path manual."""
    if not kata_kunci: return None

    # Path absolut folder assets (asumsi assets sejajar dengan app/)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assets_dir = os.path.join(base_dir, "assets")

    # 1. Cek path manual
    if os.path.exists(kata_kunci):
        return os.path.abspath(kata_kunci)

    # 2. Cari di assets
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
