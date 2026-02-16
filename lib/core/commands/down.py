from app.utility.down_osint import install_osint_module
from app.utility.load_var import load_variable
from app.utility.colors import C

# Download all OSINT modules from the repo
# The OSINT structure will be applied according to the storm logic rules.


def execute(args, context):
    cmd = args[0].lower() if args else ""

    if not cmd:
        print(f"{C.ERROR}[!] ERROR: Not module selected")
        return context

    if cmd == "osint":
        status = install_osint_module()
        if status == True:
            load_variable(context)
    else:
        print(f"{C.ERROR}[!] ERROR: {cmd} > Not found.")

    return context
