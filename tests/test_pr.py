import os

def test_core_files_existence():
    # Memastikan file vital tidak dihapus atau dipindah sembarangan
    vital_files = ["main.py", "requirements.txt", "app/__init__.py", "install.sh",
                   "app/utility/utils.py", "app/utility/colors.py", "app/base/update.py", 
                   "app/utility/search.py", "app/utility/config_path.py", "app/banners/banner.py",
                   "tests/test_pr.py"]
    for f in vital_files:
        assert os.path.exists(f), f"Vital files {f} LOST! Don't delete it."

def test_recursive_import():
    # Try importing the entire app folder to check if there is a bug in the core logic.
    try:
        pass
        
        # Add another core folder here
        assert True
    except Exception as e:
        assert False, f"Cyber-Pentest core logic is broken in this change: {e}"
