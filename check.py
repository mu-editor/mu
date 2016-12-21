import os, sys
import inspect
import subprocess
import textwrap

_exported = {}
def export(function):
    """Decorator to tag certain functions as exported, meaning
    that they show up as a command, with arguments, when this
    file is run.
    """
    _exported[function.__name__] = function
    return function

@export
def test(*args):
    """Call py.test to run the test suite
    """
    return subprocess.call(["py.test"] + list(args))

@export
def help():
    """Display all commands with their description in alphabetical order
    """
    module_doc = sys.modules['__main__'].__doc__ or "check"
    print(module_doc + "\n" + "=" * len(module_doc) + "\n")

    for command, function in sorted(_exported.items()):
        signature = inspect.signature(function)
        print("{}{}".format(command, signature))
        doc = function.__doc__
        if doc:
            print(textwrap.indent(textwrap.dedent(doc.strip("\r\n")), "    "))
        else:
            print()

def main(command="help", *args):
    """Dispatch on command name, passing all remaining parameters to the
    module-level function.
    """
    try:
        function = _exported[command]
    except KeyError:
        raise RuntimeError("No such command: %s" % command)
    else:
        return function(*args)

if __name__ == '__main__':
    sys.exit(main(*sys.argv[1:]))

"""
pyflakes *.py

pycodestyle --repeat --exclude=build/*,docs/*,mu/contrib*,mu/resources/api.py --ignore=E731,E402 .
"""
