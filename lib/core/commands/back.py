# Copyright (c) 2026 Storm Framework

# Licensed under the MIT License.

See LICENSE file in the project root for full license information.

def execute(args, context):
    if context["current_module"]:
        context["current_module"] = None
        context["current_module_name"] = ""

    return context
