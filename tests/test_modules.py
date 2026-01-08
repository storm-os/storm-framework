import os
import importlib.util
import pytest

# Path ke folder modules kamu
MODULES_DIR = "modules"

def get_all_modules():
    """Mencari semua file .py di folder modules secara otomatis."""
    modules = []
    if os.path.exists(MODULES_DIR):
        for filename in os.listdir(MODULES_DIR):
            if filename.endswith(".py") and filename != "__init__.py":
                modules.append(filename)
    return modules

@pytest.mark.parametrize("module_file", get_all_modules())
def test_module_load(module_file):
    """
    Tes ini akan mencoba me-load setiap module. 
    Jika ada kontributor yang kodenya typo/error, tes ini akan MERAH.
    """
    module_path = os.path.join(MODULES_DIR, module_file)
    module_name = module_file[:-3] # Hapus .py
    
    try:
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        foo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(foo)
        # Jika sampai sini tanpa error, berarti kode 'sehat' (bisa di-import)
        assert True
    except Exception as e:
        pytest.fail(f"Module {module_file} RUSAK/ERROR: {e}")
      
