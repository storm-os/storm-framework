import json
import hashlib
import base64
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric import ed25519

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()



def generate_folder_manifest():
    root_dir = Path(__file__).resolve().parent.parent.parent
    print(f"[*] Signature starts from: {root_dir}")

    # 1. Load Private Key dari .env
    priv_key_b64 = None
    env_path = root_dir / ".env"
    
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("STORM_PRIVKEY="):
                    priv_key_b64 = line.split("=")[1].strip()
                    break

    if not priv_key_b64:
        print("[!] Error: STORM_PRIVKEY not found in .env. Run setup.sh first!")
        return

    # 2. Scanning Files (Logika lama kamu)
    manifest = {}
    ignored_dirs = {
        '.git', '__pycache__', '.pytest_cache', 
        '.github', 'storm.db', '.gitignore', '.env'
    }

    for path in root_dir.rglob('*'):
        if path.is_file() and path.name != "signed_manifest.json":
            if not any(part in ignored_dirs for part in path.parts):
                relative_path = str(path.relative_to(root_dir))
                # Gunakan fungsi hash sha256 kamu di sini
                manifest[relative_path] = {
                    "sha256": calculate_sha256(path), 
                    "size_bytes": path.stat().st_size
                }

    # 3. Urutkan manifest agar hash JSON selalu konsisten (Penting!)
    sorted_manifest = dict(sorted(manifest.items()))

    # 4. Proses Signing
    # Convert dict ke string JSON yang rapat (compact) untuk di-hash
    manifest_string = json.dumps(sorted_manifest, sort_keys=True).encode('utf-8')
    
    # Load private key dari Base64 DER
    try:
        priv_bytes = base64.b64decode(priv_key_b64)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(priv_bytes[-32:])
        
        # Buat Signature
        signature = private_key.sign(manifest_string)
        signature_b64 = base64.b64encode(signature).decode('utf-8')
    except Exception as e:
        print(f"[!] Signing Error: {e}")
        return

    # 5. Bungkus manifest dengan Signature-nya
    final_data = {
        "metadata": {
            "version": "1.0",
            "signature": signature_b64
        },
        "files": sorted_manifest
    }

    # 6. Simpan
    output_dir = root_dir / "lib" / "core" / "database"
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = output_dir / "signed_manifest.json"

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=4)

    print(f"[+] Success! Manifest signed and saved.")
    print(f"[+] Registered files: {len(sorted_manifest)}")
