import app.utility.utils as utils


def execute(args, context):
    module_name = args[0].lower() if args else ""
    mod = utils.load_module_dynamically(module_name)

    if mod:
        context["current_module"] = mod
        context["current_module_name"] = module_name
    else:
        print(f"[-] Module: {module_name} > Not found.")

    return context
