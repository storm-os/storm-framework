import pathlib
import sys

def find_root():
    curr = pathlib.Path(__file__).resolve()
    while curr != curr.parent:
        if list(curr.glob('.git')):
            return curr
        curr = curr.parent
    return None

ROOT = find_root()

# bisa langsung di-import meskipun script dijalankan dari folder yang sangat dalam.
if ROOT and str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

