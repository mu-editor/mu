#!/usr/bin/env python3
"""
Takes a JSON representation of an API and emits elements to be inserted into a
Python list such that they conform to Scintilla's API description DSL.

HOWTO:
python mkapi.py <json file>
"""
import sys
import json


if __name__ == "__main__":
    f = sys.argv[1]
    with open(f) as api_file:
        api = json.load(api_file)
    # Sort the JSON objects so diffing code is easier to do.
    sorted_api = sorted(api, key=lambda k: k["name"])
    # Emit a representation of the API information in the format parsed by
    # the Scintilla.
    for i in sorted_api:
        name = i["name"]
        args = ", ".join(i["args"]) if i["args"] else ""
        description = i["description"].replace("\u2013", "--")
        content = repr("{}({}) \n\n{}".format(name, args, description))
        print("    _({}),".format(content))
