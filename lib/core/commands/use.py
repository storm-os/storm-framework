# Copyright (c) 2026 Storm Framework

# Licensed under the MIT License.

See LICENSE file in the project root for full license information.

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
