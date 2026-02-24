# Copyright (c) 2026 Storm Framework

# Licensed under the MIT License.

See LICENSE file in the project root for full license information.

from app.utility.search import search_modules


def execute(args, context):
    query = args[0] if args else ""
    if not query:
        print("[-] Enter file name to search!")
    else:
        search_modules(query)
    return context
