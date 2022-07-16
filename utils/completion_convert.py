"""
GitHub Issue #2291
Convert python stub file into Qscintilla autocompletion files
"""

import ast
import sys


def format_arguments(arguments):
    result = []

    for arg in arguments.args:
        result.append(f"{arg.arg}")

    if arguments.vararg:
        result.append(f"*{arguments.vararg.arg}")

    if arguments.kwarg:
        result.append(f"**{arguments.kwarg.arg}")

    return f"({', '.join(result)})"


def main():
    with open(sys.argv[1], "r") as f:
        tree = ast.parse(f.read())

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node, clean=True)
                print(
                    "{}{} {}".format(
                        node.name,
                        format_arguments(node.args),
                        " ".join(docstring.split("\n")) if docstring else "",
                    )
                )
            elif isinstance(node, ast.ClassDef):
                for node_sub in node.body:
                    if isinstance(node_sub, ast.FunctionDef) and (
                        not node_sub.name.startswith("__")
                        and not node_sub.name.endswith("__")
                    ):
                        docstring = ast.get_docstring(node_sub, clean=True)
                        print(
                            "{}.{}{} {}".format(
                                node.name,
                                node_sub.name,
                                format_arguments(node_sub.args),
                                " ".join(docstring.split("\n")) if docstring else "",
                            )
                        )


if __name__ == "__main__":
    main()
