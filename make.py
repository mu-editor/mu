import os, sys
import fnmatch
import inspect
import shutil
import subprocess
import textwrap

INCLUDE_PATTERNS = {
    "*.py"
}
EXCLUDE_PATTERNS = {
    r"build\*",
    r"docs\*",
    r"mu\contrib\*",
    r"mu\resources\api.py",
}

def _walk(start_from=".", include_patterns=None, exclude_patterns=None):
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

def _check_code(executable, *args):
    for filepath in _walk("mu", INCLUDE_PATTERNS, EXCLUDE_PATTERNS):
        print(filepath)
        subprocess.call([executable, filepath] + list(args))
    for filepath in _walk("tests", INCLUDE_PATTERNS, EXCLUDE_PATTERNS):
        print(filepath)
        subprocess.call([executable, filepath] + list(args))

def _rmtree(dirpath):
    try:
        shutil.rmtree(dirpath)
    except FileNotFoundError:
        pass

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
    """Call py.test to run the test suite with additional args
    """
    print("\n\ntest")
    return subprocess.call(["py.test.exe"] + list(args))

@export
def coverage(*args):
    """Call py.test with coverage turned on
    """
    print("\n\ncoverage")
    return subprocess.call(["py.test.exe", "--cov-config", ".coveragerc", "--cov-report", "term-missing", "--cov=mu", "tests/"])

@export
def pyflakes(*args):
    """Call pyflakes on all .py files outside the docs and contrib directories
    """
    print("\n\npyflakes")
    return _check_code("pyflakes.exe", *args)

@export
def pycodestyle(*args):
    """Call pyflakes on all .py files outside the docs and contrib directories
    """
    print("\n\nPEP8")
    args = ("--ignore=E731,E402",) + args
    return _check_code("pycodestyle.exe", *args)

@export
def pep8(*args):
    return pycodestyle(*args)

@export
def check(*args):
    """Run pyflakes + pycodestyle
    """
    print("\n\nCheck")
    pyflakes(*args)
    pycodestyle(*args)
    coverage(*args)

@export
def clean(*args):
    """Clean up any build artefacts
    """
    print("\n\nClean")
    _rmtree("build")
    _rmtree("dist")
    _rmtree("mu.egg-info")
    _rmtree("coverage")
    _rmtree("docs/build")

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
