"""
GitHub Issue #2291
Convert python stub file into Qscintilla autocompletion files
"""

import argparse
import ast
import pathlib
from glob import glob
from os.path import isdir, sep


def check_function_is_magic(fn):
    return fn.name.startswith("__") and fn.name.endswith("__")


def format_docstring(node):
    docstring = ast.get_docstring(node, clean=True)
    return " ".join(doc.strip() for doc in docstring.split("\n")) if docstring else ""


def format_signature(arguments):
    result = []

    result.extend(f"{arg.arg}" for arg in arguments.args)

    if arguments.vararg:
        result.append(f"*{arguments.vararg.arg}")

    if arguments.kwarg:
        result.append(f"**{arguments.kwarg.arg}")

    return f"({', '.join(result)})"


def format_function(node):
    return r"{}{} \n{}".format(
        node.name, format_signature(node.args), format_docstring(node)
    )


def format_methods(node_class):
    result = []

    for node_sub in node_class.body:
        if isinstance(node_sub, ast.FunctionDef) and not check_function_is_magic(
            node_sub
        ):
            result.append(
                r"{}.{}{} \n{}".format(
                    node_class.name,
                    node_sub.name,
                    format_signature(node_sub.args),
                    format_docstring(node_sub),
                )
            )

    return result


def main(arguments):
    assert isdir(arguments.stub_dir)

    result = []

    for stub in glob(f"{arguments.stub_dir}{sep}*.py"):
        with open(stub, "r") as fin:
            tree = ast.parse(fin.read())

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    result.append(format_function(node))

                elif isinstance(node, ast.ClassDef):
                    result.extend(format_methods(node))

    with arguments.output as fout:
        # FIXME fix this hack with ast.unparse when version is bumped to >= 3.9
        fout.write(
            # FIXME what should be the variable name? make this another argument to the script?
            "MICROBIT_APIS = [{}]".format(
                ", ".join(fr'_("{doc.strip()}")' for doc in result)
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("stub_dir", type=pathlib.Path)
    parser.add_argument("output", type=argparse.FileType("w"))

    main(parser.parse_args())
