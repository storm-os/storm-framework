import os
import sys

from app.utility.colors import C

try:
    from script.OSINT.storm import StormOSModuleRunner
except ImportError as e:
    print(f"[*] Run {C.SUCCESS}down OSINT{C.RESET} before using it.")
    print(f"{C.ERROR}[x] ERROR: {e}{C.RESET}")



REQUIRED_OPTIONS = {
        "EMAIL": ""
}



def execute(options):
    target_email = options.get("EMAIL")
    runner = StormOSModuleRunner()

    if target_email:
        runner.set_option("EMAIL", target_email)
        runner.run_module()
    else:
        print(f"{C.ERROR}[x] ERROR: EMAIL is not set. Use 'set EMAIL <target>'{C.RESET}")
