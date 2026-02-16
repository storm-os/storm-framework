from app.utility.load_var import load_variable
from app.utility.update import run_update
from app.utility.verify import run_verif
from app.utility.colors import C


def execute(args, context):
    cmd = args[0].lower() if args else ""

    if not cmd:
        print(f"{C.ERROR}[!] ERROR: Not module selected")
        return context

    if cmd == "update":
        run_update()
    elif cmd == "verify":
        run_verif()
    elif cmd == "restart":
        load_variable()
    else:
        print(f"{C.ERROR}[!] ERROR: {cmd} > Not found.")

    return context
