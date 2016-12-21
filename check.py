import os, sys
import fnmatch
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

def walk(start_from=".", include_patterns=None, exclude_patterns=None):
    _include_patterns = include_patterns or set(["*"])
    _exclude_patterns = exclude_patterns or set()

    for dirpath, dirnames, filenames in os.walk("mu"):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if not any(fnmatch.fnmatch(filepath, pattern) for pattern in include_patterns):
                continue
            if any (fnmatch.fnmatch(filepath, pattern) for pattern in exclude_patterns):
                continue
            yield filepath

INCLUDE_PATTERNS = {
    "*.py"
}
EXCLUDE_PATTERNS = {
    r"build\*",
    r"docs\*",
    r"mu\contrib\*",
    r"mu\resources\api.py",
}

@export
def test(*args):
    """Call py.test to run the test suite with additional args
    """
    return subprocess.call(["py.test.exe"] + list(args))

def _check(executable, *args):
    for filepath in walk("mu", INCLUDE_PATTERNS, EXCLUDE_PATTERNS):
        subprocess.call([executable, filepath] + list(args))
    for filepath in walk("tests", INCLUDE_PATTERNS, EXCLUDE_PATTERNS):
        subprocess.call([executable, filepath] + list(args))

@export
def pyflakes(*args):
    """Call pyflakes on all .py files outside the docs and contrib directories
    """
    return _check("pyflakes.exe", *args)

@export
def pycodestyle(*args):
    """Call pyflakes on all .py files outside the docs and contrib directories
    """
    args = ("--ignore=E731,E402",) + args
    return _check("pycodestyle.exe", *args)

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
