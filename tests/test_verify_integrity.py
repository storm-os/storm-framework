import hashlib
import json
from pathlib import Path
import pytest

@pytest.mark.core
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@pytest.mark.security
def test_verify_repo_integrity():
    # Setup Path
    root_dir = Path(__file__).resolve().parent.parent
    manifest_path = root_dir / "tests" / "database" / "signed_manifest.json"
    
    # 1. Make sure the database manifest already exists
    if not manifest_path.exists():
        pytest.fail("Database manifest does not exist yet! Run the generator first..")

    # 2. Load old manifest
    with open(manifest_path, "r") as f:
        old_manifest = json.load(f)

    # 3. Scan folder now
    current_manifest = {}
    ignored = {'.git', '__pycache__', '.pytest_cache', '.github', 'database'}
    
    for path in root_dir.rglob('*'):
        if path.is_file() and not any(p in path.parts for p in ignored):
            rel_path = str(path.relative_to(root_dir))
            current_manifest[rel_path] = calculate_sha256(path)

    # 4. Compare!
    old_files = set(old_manifest.keys())
    new_files = set(current_manifest.keys())

    # Check for missing files
    missing = old_files - new_files
    # Check for new files that are not yet registered
    added = new_files - old_files
    # Check files whose contents have changed (different hashes)
    changed = [f for f in (old_files & new_files) if old_manifest[f]['sha256'] != current_manifest[f]]

    # 5. Reporting
    error_msg = []
    if missing: error_msg.append(f"File missing: {missing}")
    if added: error_msg.append(f"New file (untracked): {added}")
    if changed: error_msg.append(f"File modified (Hash mismatch): {changed}")

    assert not error_msg, "\n".join(error_msg)
  
