from app.utility.restart import run_restart
from app.utility.update import run_update
from app.utility.verify import run_verif
from app.utility.colors import C


def execute(args, context):
    cmd = args[0].lower() if args else ""

    if not cmd:
        print(f"{C.ERROR}[!] ERROR: Not module selected")
        return context

    if cmd == "update":
        status = run_update()
        if status:
            run_restart(context)
    elif cmd == "verify":
        run_verif()
    elif cmd == "restart":
        run_restart(context)
    else:
        print(f"{C.ERROR}[!] ERROR: {cmd} > Not found.")

    return context
