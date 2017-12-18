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
    "build/*",
    "docs/*",
    "mu/contrib/*",
    "mu/resources/api.py",
}
_exported = {}


def _walk(
    start_from=".",
    include_patterns=None,
    exclude_patterns=None,
    recurse=True
):
    if include_patterns:
        _include_patterns = set(os.path.normpath(p) for p in include_patterns)
    else:
        _include_patterns = set()
    if exclude_patterns:
        _exclude_patterns = set(os.path.normpath(p) for p in exclude_patterns)
    else:
        _exclude_patterns = set()

    for dirpath, dirnames, filenames in os.walk(start_from):
        for filename in filenames:
            filepath = os.path.normpath(os.path.join(dirpath, filename))

            if not any(fnmatch.fnmatch(filepath, pattern)
                       for pattern in _include_patterns):
                continue

            if any(fnmatch.fnmatch(filepath, pattern)
                   for pattern in _exclude_patterns):
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
        print("Removing directory", dirpath)
        shutil.rmtree(dirpath)
        pass
    except OSError:
        if cascade_errors:
            raise


def _rmfiles(start_from, pattern):
    """Remove files from a directory and its descendants

    Starting from `start_from` directory and working downwards,
    remove all files which match `pattern`, eg *.pyc
    """
    for filepath in _walk(start_from, {pattern}):
        print("Removing", filepath)
        os.remove(filepath)


def export(function):
    """Decorator to tag certain functions as exported, meaning
    that they show up as a command, with arguments, when this
    file is run.
    """
    _exported[function.__name__] = function
    return function


@export
def test(*pytest_args):
    """Run the test suite

    Call py.test to run the test suite with additional args
    """
    print("\ntest")
    return subprocess.call([PYTEST] + list(pytest_args))


@export
def coverage():
    """View a report on test coverage

    Call py.test with coverage turned on
    """
    print("\ncoverage")
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
def pyflakes(*pyflakes_args):
    """Run the PyFlakes code checker

    Call pyflakes on all .py files outside the docs and contrib directories
    """
    print("\npyflakes")
    return _check_code(PYFLAKES, *args)


@export
def pycodestyle(*pycodestyle_args):
    """Run the PEP8 style checker
    """
    print("\nPEP8")
    args = ("--ignore=E731,E402",) + args
    return _check_code(PYCODESTYLE, *args)


@export
def pep8(*pep8_args):
    """Run the PEP8 style checker
    """
    return pycodestyle(*args)


@export
def check():
    """Run all the checkers and tests
    """
    print("\nCheck")
    pyflakes()
    pycodestyle()
    coverage()


@export
def clean():
    """Reset the project and remove auto-generated assets
    """
    print("\nClean")
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
        doc = function.__doc__
        if doc:
            first_line = doc.splitlines()[0]
        else:
            first_line = ""
        print("make {} - {}".format(command, first_line))


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
