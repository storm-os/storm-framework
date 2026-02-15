from app.utility.down_osint import install_osint_module
from app.utility.colors import C

# Download all OSINT modules from the repo
# The OSINT structure will be applied according to the storm logic rules.


def execute(args, context):
    cmd = args[0].lower() if args else ""

    if not cmd:
        print(f"{C.ERROR}[!] ERROR: Not module selected")
        return context

    if cmd == "osint":
        install_osint_module()
    else:
        print(f"{C.ERROR}[!] ERROR: {cmd} > Not found.")

    return context
