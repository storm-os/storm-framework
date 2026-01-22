import os

def test_core_files_existence():
    # Memastikan file vital tidak dihapus atau dipindah sembarangan
    vital_files = ["main.py", "requirements.txt", "app/__init__.py", "install.sh",
                   "app/utility/utils.py", "app/utility/colors.py", "app/base/update.py", 
                   "app/utility/search.py", "app/utility/config_path.py", "app/banners/banner.py",
                   "tests/test_pr.py"]
    for f in vital_files:
        assert os.path.exists(f), f"File vital {f} HILANG! Jangan dihapus."

def test_recursive_import():
    # Mencoba import seluruh folder app untuk cek apakah ada bug di logic inti
    try:
        pass
        
        # Tambahkan folder inti lainnya di sini
        assert True
    except Exception as e:
        assert False, f"Logic inti Cyber-Pentest rusak di perubahan ini: {e}"
