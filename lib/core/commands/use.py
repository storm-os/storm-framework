import app.utility.utils as utils


def execute(args, context):
    module_name = args[0].lower() if args else ""
    mod = utils.load_module_dynamically(module_name)

    if mod:
        # JANGAN cuma bikin variabel, tapi MASUKKAN ke context
        context["current_module"] = mod
        context["current_module_name"] = module_name
    else:
        print(f"[-] Module: {module_name} > Not found.")

    # Sekarang context sudah berisi data yang baru
    return context
