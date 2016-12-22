#!python3
import os
import sys
import fnmatch
import inspect
import shutil
import subprocess
import textwrap

PYTEST = "pytest"
PYFLAKES = "pyflakes"
PYCODESTYLE = "pycodestyle"

INCLUDE_PATTERNS = {
    "*.py"
}
EXCLUDE_PATTERNS = {
    r"build\*",
    r"docs\*",
    r"mu\contrib\*",
    r"mu\resources\api.py",
}
_exported = {}


def _walk(
    start_from=".",
    include_patterns=None,
    exclude_patterns=None,
    recurse=True
):
    _include_patterns = include_patterns or set(["*"])
    _exclude_patterns = exclude_patterns or set()

    for dirpath, dirnames, filenames in os.walk(start_from):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)

            includes = [fnmatch.fnmatch(filepath, pattern)
                        for pattern in _include_patterns]
            if not any(includes):
                continue

            excludes = [fnmatch.fnmatch(filepath, pattern)
                        for pattern in _exclude_patterns]
            if any(excludes):
                continue

            yield filepath

        if not recurse:
            break


def _check_code(executable, *args):
    for filepath in _walk(".", INCLUDE_PATTERNS, EXCLUDE_PATTERNS, False):
        print(filepath)
        subprocess.call([executable, filepath] + list(args))
    for filepath in _walk("mu", INCLUDE_PATTERNS, EXCLUDE_PATTERNS):
        print(filepath)
        subprocess.call([executable, filepath] + list(args))
    for filepath in _walk("tests", INCLUDE_PATTERNS, EXCLUDE_PATTERNS):
        print(filepath)
        subprocess.call([executable, filepath] + list(args))


def _rmtree(dirpath, cascade_errors=False):
    try:
        shutil.rmtree(dirpath)
    except OSError:
        if cascade_errors:
            raise


def _rmfiles(start_from, pattern):
    for filepath in _walk(".", {"*.pyc"}):
        print(filepath)
        os.remove(filepath)


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
    return subprocess.call([PYTEST] + list(args))


@export
def coverage(*args):
    """Call py.test with coverage turned on
    """
    print("\n\ncoverage")
    return subprocess.call([
        PYTEST,
        "--cov-config",
        ".coveragerc",
        "--cov-report",
        "term-missing",
        "--cov=mu",
        "tests/"
    ])


@export
def pyflakes(*args):
    """Call pyflakes on all .py files outside the docs and contrib directories
    """
    print("\n\npyflakes")
    return _check_code(PYFLAKES, *args)


@export
def pycodestyle(*args):
    """Call pyflakes on all .py files outside the docs and contrib directories
    """
    print("\n\nPEP8")
    args = ("--ignore=E731,E402",) + args
    return _check_code(PYCODESTYLE, *args)


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
    _rmfiles(".", "*.pyc")


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
