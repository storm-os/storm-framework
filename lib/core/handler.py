import importlib
import os
from app.utility.colors import C


def execute(cmd, args, context):
    """Fungsi pusat untuk mencari dan menjalankan file perintah."""
    # Format path: lib/core/commands/use.py
    cmd_path = os.path.join("lib", "core", "commands", f"{cmd}.py")

    if os.path.exists(cmd_path):
        try:
            # Import dinamis sesuai perintah
            module = importlib.import_module(f"lib.core.commands.{cmd}")
            # Panggil fungsi utama di dalam file tersebut
            return module.execute(args, context)
        except Exception as e:
            print(f"{C.ERROR}[-] Error in command '{cmd}': {e}")
            return context

    # Jika file tidak ditemukan di folder commands
    return None
