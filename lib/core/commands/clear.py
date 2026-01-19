import os
from app.banners.banner import get_random_banner
import app.base.config_ui as config_ui

def execute(args, context):
    # Bersihkan layar sesuai OS
    os.system('cls' if os.name == 'nt' else 'clear')

    # Tampilkan ulang identitas tools
    print(get_random_banner())
    config_ui.stormUI()

    return context
