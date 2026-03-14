import sys
from pathlib import Path

#
# rootmap best jump shortcut to find root folder
# make sure to use it if needed to access files in other folders
#
def find_and_inject_root():
    p = Path(__file__).resolve()
    for parent in p.parents:
        if (parent / '.git').exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))

            return parent

    return None

ROOT = find_and_inject_root()
###
# directly use example:
# from rootmap import ROOT
# root = os.path.join(ROOT, "")
###
