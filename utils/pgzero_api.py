#!/usr/bin/env python3
"""
Given a list of modules, extracts the help into a json file to be turned into
an API list for Mu.
"""
import json
import inspect
import importlib


modules = ['screen', 'music', 'keyboard', 'clock', 'animation', 'actor', ]

api = []

for module in modules:
    m = importlib.import_module('pgzero.{}'.format(module))
    content = [attr for attr in dir(m) if not attr.startswith('_')]
    # Work out what each member of the module is.
    for attr in content:
        obj = getattr(m, attr)
        name = ''
        try:
            name = obj.__name__
        except:
            print(obj)
        try:
            args = [a.replace('(', '').replace(')', '') for a in
                    str(inspect.signature(obj)).split(', ')]
        except:
            args = None
        description = inspect.getdoc(obj)
        if name and description:
            api.append({
                'name': module + '.' + name,
                'args': args,
                'description': description,
            })


with open('pgzero_api.json', 'w') as output:
    json.dump(api, output, indent=2)
