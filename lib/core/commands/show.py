import app.utility.utils as utils
from app.utility.colors import C


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
            req = getattr(current_module, "REQUIRED_OPTIONS", {})
            for var_name, desc in req.items():
                val = options.get(var_name, "unset")
                print(f"{var_name:<12} {val:<25} {desc}")
        else:
            for k, v in options.items():
                val = v if v else "unset"
                print(f"{k:<12} {val:<25} Global Variable")
        print("")

    # 3. show db (Gudang Data)
    elif target_show == "db":
        # Cek apakah ada argumen setelah 'db'
        # Contoh: 'show db CVE-2017-0144' -> args[0] adalah CVE-ID nya
        if len(args) > 1:
            target_id = args[1]

            # Jika argumennya adalah 'cve', tampilkan katalog (semua)
            if target_id.lower() == "cve":
                utils.cve_summary()
            else:
                # Jika argumennya adalah ID CVE (misal: CVE-2017-0144)
                # Tampilkan detail satu per satu
                utils.detail_cve(target_id)
        else:
            # Jika cuma ketik 'show db' tanpa argumen
            print(
                f"{C.INPUT}[*] Penggunaan: show db cve (untuk list) atau show db <CVE-ID> (untuk detail)"
            )

    # 4. show <category_name>
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
