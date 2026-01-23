import os
import json
import hashlib
from pathlib import Path
import pytest

def calculate_sha256(file_path):
    """Menghitung hash SHA-256 dari sebuah file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read files in chunks to save RAM for large files
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def test_generate_folder_manifest():
    root_dir = Path(__file__).resolve().parent.parent
    print(f"Scanning starts from: {root_dir}")
   
    manifest = {}
    
    # List of folders to ignore (example: .git, __pycache__, .pytest_cache)
    ignored_dirs = {'.git', '__pycache__', '.pytest_cache', '.github'}

    for path in root_dir.rglob('*'):
        if path.is_file() and not any(part in ignored_dirs for part in path.parts):
            relative_path = str(path.relative_to(root_dir))
            manifest[relative_path] = {
                "sha256": calculate_sha256(path),
                "size_bytes": path.stat().st_size
            }

    # Save to JSON file
    with open("signed_manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)
    
    assert os.path.exists("signed_manifest.json")
  
