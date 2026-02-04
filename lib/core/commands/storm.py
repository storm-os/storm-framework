from app.utility.update import run_update
from app.utility.colors import C

def execute(args, context):
    cmd = args[0].lower() if args else ""

    if not cmd:
        print(f"{C.ERROR}[!] ERROR: Not module selected")
        return context
        
    def cmd == "update":
        run_update()
    
    return context
