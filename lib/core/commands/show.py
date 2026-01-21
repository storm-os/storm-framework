import app.utility.utils as utils
from app.utility.colors import C
from lib.sqlite.helper_db import StormDatabase

def execute(args, context):
    target_show = args[0].lower() if args else ""
    current_module = context["current_module"]
    current_module_name = context["current_module_name"]
    options = context["options"]

    if not target_show:
        print(f"{C.ERROR}[!] No modules selected.")
        return context

    # 1. show modules
    if target_show == "modules":
        categories = utils.get_categories()
        print(f"\n{C.HEADER}--- Categories ---")
        for cat in categories:
            print(f"  - {cat}")
        print(f"\n{C.INPUT}Use 'show <category_name>' to see modules.")
        print("")

    # 2. show options
    elif target_show == "options":
        header_name = current_module_name if current_module else "GLOBAL"
        print(f"\n{C.HEADER}MODULE OPTIONS ({header_name}):")
        print(f"{'Name':<12} {'Current Setting':<25} {'Description'}")
        print(f"{'-'*12} {'-'*25} {'-'*15}")

        if current_module:
            req = getattr(current_module, 'REQUIRED_OPTIONS', {})
            for var_name, desc in req.items():
                val = options.get(var_name, "unset")
                print(f"{var_name:<12} {val:<25} {desc}")
        else:
            for k, v in options.items():
                val = v if v else "unset"
                print(f"{k:<12} {val:<25} Global Variable")
        print("")

    # 4. show db (Gudang Data)
    elif target_show == "db" or target_show == "storage":

        try:
            db = StormDatabase()

            # Sub-argumen, misal: show db targets
            sub_target = args[1].lower() if len(args) > 1 else "summary"

            if sub_target == "target":
                data = db.fetch_all_targets()
                print(f"\n{C.HEADER}--- Target Warehouse ---")
                print(f"{'Address':<20} | {'Port':<6} | {'Service':<12}")
                for row in data:
                    print(f"{row[0]:<20} | {row[1]:<6} | {row[2]:<12}")

            elif sub_target == "cve":
                data = db.fetch_all_cve()
                print(f"\n{C.HEADER}--- CVE Library ---")
                for row in data:
                    print(f"  [{row[2]}] {row[0]}: {row[1][:40]}...")

            else:
                # Ringkasan gudang jika cuma ketik 'show db'
                print(f"\n{C.HEADER}--- Storage Summary ---")
                print(f"  Target : {len(db.fetch_all_targets())} entries")
                print(f"  CVEs   : {len(db.fetch_all_cve())} entries")
                print(f"\n{C.INPUT}Use 'show db target' or 'show db cve' for details.")

        except Exception as e:
            print(f"{C.ERROR}[-] Database Error: {e}")
        print("")

    # 3. show <category_name>
    else:
        module_files = utils.get_modules_in_category(target_show)
        if module_files:
            print(f"\n{C.HEADER}Modules in {target_show}:")
            for mod in module_files:
                print(f"  - {mod}")
            print("")
        else:
            print(f"{C.ERROR}[-] Category or option '{target_show}' not found.")

    return context
