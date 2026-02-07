
from app.utility.colors import C


try:
    from script.osint.handstorm import StormOSModuleRunner
except ImportError as e:
    print(f"[*] Run {C.SUCCESS}down OSINT{C.RESET} before using it.")
    print(f"{C.ERROR}[x] ERROR: {e}{C.RESET}")



REQUIRED_OPTIONS = {
        "EMAIL": ""
}
def execute(options):
    mail = options.get("EMAIL")
    runner = StormOSModuleRunner()

    if mail:
        runner.str(set_option(mail))
        runner.run_module()
    else:
        print(f"{C.ERROR}[x] ERROR: EMAIL is not set. Use 'set EMAIL <target>'{C.RESET}")
