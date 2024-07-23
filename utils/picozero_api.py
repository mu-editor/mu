#!/usr/bin/env python3
"""
Given a list of modules, extracts the help into a json file to be turned into
an API list for Mu.

STEPS:
1. Transform docstring to Google style coding convention
pip install docconvert
docconvert --in-place picozero.py 
mv picozero.py to picozero_g.py

2. Execute this script and copy&paste the printed to modes/api/pico.py
"""
import json
import ast
from pprint import pprint

api = []

class Analayzer(ast.NodeVisitor):
    def __init__(self):
        self.objs = []
        self.cls_name = ''

    def visit_ClassDef(self, node):
        doc_string = ast.get_docstring(node)
        if doc_string:
            self.objs.append({
                "name": 'picozero' + '.' + node.name,
                "args": [],
                "description": doc_string,
            })
            self.cls_name = node.name
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if node.name == '__init__':
            if hasattr(node, 'args'):
                args = [arg.arg for arg in node.args.args]
                if args != ['self']:
                    self.objs[len(self.objs)-1]['args'] = args[1:]

        doc_string = ast.get_docstring(node)
        if doc_string:
            obj = {
                "name": '',
                "args": [],
                "description": doc_string,
            }
            if hasattr(node, 'args'):
                obj['args'] = [arg.arg for arg in node.args.args]
                if len(node.args.defaults): # Fill the default value of each arg
                    for idx, default in enumerate(node.args.defaults):
                        # If the arg has default value, mark it's not mandatory
                        obj['args'][-(idx+1)] = '[' + obj['args'][-(idx+1)] + ']'
                        
                if obj['args'] == ['self']:
                    obj['name'] = self.cls_name + "." + node.name
                    obj['args'] = []
                elif self.cls_name:  # If a method in class
                    obj['name'] = self.cls_name + "." + node.name
                    obj['args'] = obj['args'][1:]
                else:
                    obj['name'] = 'picozero' + "." + node.name
            self.objs.append(obj)
        self.generic_visit(node)

    def report(self):
        pprint(self.objs)

with open("picozero_g.py", "r") as f:
    cls_name = ''
    p = ast.parse(f.read())

    anal = Analayzer()
    anal.visit(p)
    anal.report()

with open("picozero_api.json", "w") as output:
    json.dump(anal.objs, output, indent=2)
