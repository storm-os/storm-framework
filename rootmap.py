import sys
from pathlib import Path

def find_and_inject_root():
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / '.git').exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return None

ROOT = find_and_inject_root()
