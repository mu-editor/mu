"""
GitHub Issue #2291
Convert python stub file into Qscintilla autocompletion files
"""

import importlib.util
import sys
from inspect import getmembers, isclass, isfunction, signature

spec = importlib.util.spec_from_file_location("module", sys.argv[1])
module = importlib.util.module_from_spec(spec)
# sys.modules["testcode"] = module
spec.loader.exec_module(module)


def format_docstring(x):
    return (
        " ".join(sentence.strip() for sentence in x.__doc__.split("\n"))
        if x.__doc__
        else ""
    )


def main():
    print(
        list(
            f"{name}{str(signature(fn))} {format_docstring(fn)}".strip()
            for name, fn in getmembers(module, isfunction)
        )
        + list(
            f"{class_name}.{class_method}{str(signature(fn))} {format_docstring(fn)}".strip()
            for class_name, _class in getmembers(module, isclass)
            for class_method, fn in getmembers(_class, isfunction)
        )
    )


if __name__ == "__main__":
    main()
