import textwrap
import versi as v
import app.utility.utils as utils
from app.utility.colors import C

def show_about():
    print(f"\n{C.HEADER}==========================================================================")
    print(f"{C.SUCCESS}                        CYBER PENTEST FRAMEWORK")
    print(f"{C.HEADER}==========================================================================")
    print(f"{C.INPUT}      owner                     : Elzy")
    print(f"{C.INPUT}      Contributor               : There isn't any yet")
    print(f"{C.INPUT}      Purpose                   : All-in-One Pentest Tools")
    print(f"{C.INPUT}      Version                   : {v.VERSION}")
    print(f"{C.INPUT}      GitHub                    : github.com/storm-os/Cyber-Pentest")
    print(f"{C.HEADER}==========================================================================\n")

def show_help():
    print(f"""
{C.HEADER}==========================================================================
{C.SUCCESS}                             COMMAND GUIDE
{C.HEADER}==========================================================================
{C.INPUT}
  help                          : Displaying the manual
  show options                  : View the variables that have been set
  show modules                  : Displaying module categories
  show <name_categories>        : Displays the complete contents
  search <filename>             : To search for files
  about                         : Information Development
  back                          : Back from current position
  clear                         : Clear command line
  exit                          : Exit the application
{C.INPUT}
  use <nama_modul>              : Selecting a module
  set <key> <val>               : Filling in the parameters
  run / exploit                 : Run the selected module

{C.HEADER}==========================================================================
    """)


def stormUI():
    total = utils.count_modules()
    stats = utils.count_by_category()
    clean_stats = " | ".join([f"{cat.upper()}: {val}" for cat, val in stats.items()])
    full_text = f"[!] MODULE: {total} | {clean_stats}"
    wrapped_text = textwrap.fill(full_text, width=50, subsequent_indent="        ")
    print(f"{C.HEADER}\n+-- --=[ {C.INPUT}{wrapped_text} {C.HEADER}]=--")
    print("")
    print("The Cyber Pentest is a storm-os Open Source Project")
    print(f"Run {C.SUCCESS}about{C.RESET} to view dev information.")
    print("")



