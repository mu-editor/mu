#!/usr/bin/env python3
"""
Given a list of modules, extracts the help into a json file to be turned into
an API list for Mu.
"""
import json
import inspect
import importlib


modules = [
    "random",
    "sys",
    "os",
    "json",
    "socket",
    "datetime",
    "collections",
    "datetime",
    "array",
    "itertools",
    "functools",
    "os.path",
    "csv",
    "time",
    "argparse",
    "base64",
    "hashlib",
    "uuid",
    "turtle",
]

api = []

for module in modules:
    m = importlib.import_module(module)
    content = [attr for attr in dir(m) if not attr.startswith("_")]
    # Work out what each member of the module is.
    for attr in content:
        obj = getattr(m, attr)
        name = ""
        try:
            name = obj.__name__
        except Exception as ex:
            print(ex)
            print(obj)
        try:
            args = [
                a.replace("(", "").replace(")", "")
                for a in str(inspect.signature(obj)).split(", ")
            ]
        except Exception as ex:
            print(ex)
            print(obj)
            args = None
        description = inspect.getdoc(obj)
        if name and description:
            api.append(
                {
                    "name": module + "." + name,
                    "args": args,
                    "description": description,
                }
            )


with open("python_api.json", "w") as output:
    json.dump(api, output, indent=2)
