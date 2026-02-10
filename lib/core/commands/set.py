import app.utility.utils as utils


def execute(args, context):
    options = context["options"]

    if len(args) >= 2:
        var_name = args[0].upper()
        var_value = args[1]

        # Logika otomatis untuk PATH (seperti di main.py lama kamu)
        if "PATH" in var_name or var_name == "PASS":
            found_path = utils.resolve_path(var_value)
            if found_path:
                options[var_name] = found_path
                print(f"{var_name} => {found_path}")
            else:
                print(f"[-] File '{var_value}' not found!")
        else:
            options[var_name] = var_value
            print(f"{var_name} => {var_value}")
    else:
        print(f"[!] Use: set <VARIABLE> <VALUE>")

    context["options"] = options
    return context
