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
    with open("test.py", "w") as fout:
        result = []

        with open(sys.argv[1], "r") as fin:
            tree = ast.parse(fin.read())

            for node in ast.iter_child_nodes(tree):
                if isinstance(node, ast.FunctionDef):
                    docstring = ast.get_docstring(node, clean=True)
                    result.append(
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
                            result.append(
                                "{}.{}{} {}".format(
                                    node.name,
                                    node_sub.name,
                                    format_arguments(node_sub.args),
                                    " ".join(docstring.split("\n"))
                                    if docstring
                                    else "",
                                )
                            )

        # FIXME fix this hack with ast.unparse when version is bumped to >= 3.9
        fout.write(
            "MICROBIT_APIS = [{}]".format(
                ", ".join(fr'_("{doc.strip()}")' for doc in result)
            )
        )


if __name__ == "__main__":
    main()
