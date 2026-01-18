import versi as v
from app.utility.colors import C

def show_about():
    print(f"\n{C.HEADER}=====================================================================")
    print(f"{C.SUCCESS}                    CYBER PENTEST FRAMEWORK")
    print(f"{C.HEADER}=====================================================================")
    print(f"{C.INPUT}      owner                  : Elzy")
    print(f"{C.INPUT}      Contributor            : There isn't any yet")
    print(f"{C.INPUT}      Purpose                : All-in-One Pentest Tools")
    print(f"{C.INPUT}      Version                : {v.VERSION}")
    print(f"{C.INPUT}      GitHub                 : github.com/storm-os/Cyber-Pentest")
    print(f"{C.HEADER}=====================================================================\n")

def show_help():
    print(f"""
{C.HEADER}============================= COMMAND GUIDE ===============================
{C.MENU} Help command:
  help                          : Displaying the manual
  show options                  : View the variables that have been set
  show modules                  : Displaying module categories
  show <name_categories>        : Displays the complete contents
  search <filename>             : To search for files
  about                         : Information Development
  back                          : Back from current position
  exit                          : Exit the application

{C.MENU} Command Workflow:
  use <nama_modul>              : Selecting a module
  set <key> <val>               : Filling in the parameters
  run / exploit                 : Run the selected module
{C.HEADER}===========================================================================
    """)

