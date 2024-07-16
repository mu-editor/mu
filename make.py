#!python3
import os
import sys
import fnmatch
import re
import shutil
import subprocess

PYTEST = "pytest"
FLAKE8 = "flake8"
BLACK = "black"
BLACK_FLAGS = ["-l", "79", "--exclude=mu/contrib/"]
PYGETTEXT = os.path.join(sys.base_prefix, "tools", "i18n", "pygettext.py")

INCLUDE_PATTERNS = {"*.py"}
EXCLUDE_PATTERNS = {
    "build/*",
    "docs/*",
    "mu/contrib/*",
    "mu/modes/api/*",
    "utils/*",
}
_exported = {}


def _walk(
    start_from=".", include_patterns=None, exclude_patterns=None, recurse=True
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

            if not any(
                fnmatch.fnmatch(filepath, pattern)
                for pattern in _include_patterns
            ):
                continue

            if any(
                fnmatch.fnmatch(filepath, pattern)
                for pattern in _exclude_patterns
            ):
                continue

            yield filepath

        if not recurse:
            break


def _rmtree(dirpath, cascade_errors=False):
    try:
        shutil.rmtree(dirpath)
    except OSError:
        if cascade_errors:
            raise


def _rmfiles(start_from, pattern):
    """Remove files from a directory and its descendants

    Starting from `start_from` directory and working downwards,
    remove all files which match `pattern`, eg *.pyc
    """
    for filepath in _walk(start_from, {pattern}):
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

    Call py.test to run the test suite with additional args.
    The subprocess runner will raise an exception if py.test exits
    with a failure value. This forces things to stop if tests fail.
    """
    print("\ntest")
    os.environ["LANG"] = "en_GB.utf8"
    return subprocess.run(
        [sys.executable, "-m", PYTEST] + list(pytest_args)
    ).returncode


@export
def coverage():
    """View a report on test coverage

    Call py.test with coverage turned on
    """
    print("\ncoverage")
    os.environ["LANG"] = "en_GB.utf8"
    return subprocess.run(
        [
            sys.executable,
            "-m",
            PYTEST,
            "-v",
            "--cov-config",
            "setup.cfg",
            "--cov-report",
            "term-missing",
            "--cov=mu",
            "tests/",
        ]
    ).returncode


@export
def flake8(*flake8_args):
    """Run the flake8 code checker

    Call flake8 on all files as specified by setup.cfg
    """
    print("\nflake8")
    os.environ["PYFLAKES_BUILTINS"] = "_"
    return subprocess.run([sys.executable, "-m", FLAKE8]).returncode


@export
def tidy():
    """Tidy code with the 'black' formatter."""
    clean()
    print("\nTidy")
    for target in [
        "setup.py",
        "make.py",
        "mu",
        "package",
        "tests",
        "utils",
    ]:
        return_code = subprocess.run(
            [sys.executable, "-m", BLACK, target] + BLACK_FLAGS
        ).returncode
        if return_code != 0:
            return return_code
    return 0


@export
def black():
    """Check code with the 'black' formatter."""
    clean()
    print("\nblack")
    # Black is no available in Python 3.5, in that case let the tests continue
    try:
        import black as black_  # noqa: F401
    except ImportError as e:
        python_version = sys.version_info
        if python_version.major == 3 and python_version.minor == 5:
            print("Black checks are not available in Python 3.5.")
            return 0
        else:
            print(e)
            return 1
    for target in [
        "setup.py",
        "make.py",
        "mu",
        "package",
        "tests",
        "utils",
    ]:
        return_code = subprocess.run(
            [sys.executable, "-m", BLACK, target, "--check"] + BLACK_FLAGS
        ).returncode
        if return_code != 0:
            return return_code
    return 0


@export
def check():
    """Run all the checkers and tests"""
    print("\nCheck")
    # funcs = [clean, black, flake8, coverage]
    funcs = [clean]  # temporary for a build
    for func in funcs:
        return_code = func()
        if return_code != 0:
            return return_code
    return 0


@export
def clean():
    """Reset the project and remove auto-generated assets"""
    print("\nClean")
    _rmtree("build")
    _rmtree("dist")
    _rmtree(".eggs")
    _rmtree("docs/_build")
    _rmtree(".pytest_cache")
    _rmtree("lib")
    _rmtree(".git/avatar/")  # Created with `make video`
    _rmtree("venv-pup")  # Created wth `make macos/win64`
    # TODO: recursive __pycache__ directories
    _rmfiles(".", ".coverage")
    _rmfiles(".", "*.egg-info")
    _rmfiles(".", "*.mp4")  # Created with `make video`
    _rmfiles(".", "*.pyc")
    _rmfiles("mu/locale", "*.pot")
    _rmfiles("mu/wheels", "*.zip")
    return 0


def _translate_lang(lang):
    """Returns `value` from `lang` expected to be like 'LANG=value'."""
    match = re.search(r"^LANG=(.*)$", lang)
    if not match:
        raise RuntimeError("Need LANG=xx_XX argument.")
    value = match.group(1)
    if not value:
        raise RuntimeError("Need LANG=xx_XX argument.")
    return value


_MU_LOCALE_DIRNAME = os.path.join("mu", "locale")
_MESSAGES_POT_FILENAME = os.path.join(_MU_LOCALE_DIRNAME, "messages.pot")


@export
def translate_begin(lang=""):
    """Create/update a mu.po file for translation."""
    lang = _translate_lang(lang)
    result = _translate_extract()
    if result != 0:
        raise RuntimeError("Failed creating the messages catalog file.")

    mu_po_filename = os.path.join(
        _MU_LOCALE_DIRNAME,
        lang,
        "LC_MESSAGES",
        "mu.po",
    )
    update = os.path.exists(mu_po_filename)
    cmd = [
        "pybabel",
        "update" if update else "init",
        "-i",
        _MESSAGES_POT_FILENAME,
        "-o",
        mu_po_filename,
        "--locale={locale}".format(locale=lang),
    ]
    result = subprocess.run(cmd).returncode

    print(
        "{action} {mu_po_filename}.".format(
            action="Updated" if update else "Created",
            mu_po_filename=repr(mu_po_filename),
        )
    )
    print(
        "Review its translation strings "
        "and finalize with 'make translate_done'."
    )

    return result


_TRANSLATE_IGNORE_DIRNAMES = {
    os.path.join("mu", "modes", "api"),
    os.path.join("mu", "contrib"),
}


def _translate_ignore(dirname):
    """Return True if `dirname` files should be excluded from translation."""
    return any(dirname.startswith(dn) for dn in _TRANSLATE_IGNORE_DIRNAMES)


def _translate_filenames():
    """Returns a sorted list of filenames with translatable strings."""
    py_filenames = []
    for dirname, _, filenames in os.walk("mu"):
        if _translate_ignore(dirname):
            continue
        py_filenames.extend(
            os.path.join(dirname, fn) for fn in filenames if fn.endswith(".py")
        )
    return sorted(py_filenames)


def _translate_extract():
    """Creates the message catalog template messages.pot file."""
    cmd = [
        "pybabel",
        "extract",
        "-o",
        _MESSAGES_POT_FILENAME,
        *_translate_filenames(),
    ]
    return subprocess.run(cmd).returncode


@export
def translate_done(lang=""):
    """Compile translation strings in mu.po to mu.mo file."""
    lang = _translate_lang(lang)

    lc_messages_dirname = os.path.join(
        _MU_LOCALE_DIRNAME,
        lang,
        "LC_MESSAGES",
    )
    mu_po_filename = os.path.join(lc_messages_dirname, "mu.po")
    mu_mo_filename = os.path.join(lc_messages_dirname, "mu.mo")
    cmd = [
        "pybabel",
        "compile",
        "-i",
        mu_po_filename,
        "-o",
        mu_mo_filename,
        "--locale={locale}".format(locale=lang),
    ]
    return subprocess.run(cmd).returncode


@export
def translate_test(lang=""):
    """Run translate_done and lauch Mu in the given LANG."""
    result = translate_done(lang)
    if result != 0:
        raise RuntimeError("Failed compiling the mu.po file.")

    local_env = dict(os.environ)
    local_env["LANG"] = _translate_lang(lang)
    return subprocess.run(
        [sys.executable, "-m", "mu"], env=local_env
    ).returncode


@export
def run():
    """Run Mu from within a virtual environment"""
    clean()
    if not os.environ.get("VIRTUAL_ENV"):
        raise RuntimeError(
            "Cannot run Mu;" "your Python virtualenv is not activated"
        )
    return subprocess.run([sys.executable, "-m", "mu"]).returncode


@export
def dist():
    """Generate a source distribution and a binary wheel"""
    if check() != 0:
        raise RuntimeError("Check failed")
    print("Checks pass; good to package")
    return subprocess.run(
        [sys.executable, "setup.py", "sdist", "bdist_wheel"]
    ).returncode


@export
def publish_test():
    """Upload to a test PyPI"""
    dist()
    print("Packaging complete; upload to PyPI")
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "twine",
            "upload",
            "-r",
            "test",
            "--sign",
            "dist/*",
        ]
    ).returncode


@export
def publish_live():
    """Upload to PyPI"""
    dist()
    print("Packaging complete; upload to PyPI")
    return subprocess.run(
        [sys.executable, "-m", "twine", "upload", "--sign", "dist/*"]
    ).returncode


_PUP_PBS_URLs = {
    32: "https://github.com/indygreg/python-build-standalone/releases/download/20200822/cpython-3.7.9-i686-pc-windows-msvc-shared-pgo-20200823T0159.tar.zst",  # noqa: E501
    64: None,
}


def _build_windows_msi(bitness=64):
    """Build Windows MSI installer"""
    try:
        pup_pbs_url = _PUP_PBS_URLs[bitness]
    except KeyError:
        raise ValueError("bitness") from None
    if check() != 0:
        raise RuntimeError("Check failed")
    print("Fetching wheels")
    subprocess.check_call([sys.executable, "-m", "mu.wheels", "--package"])
    print("Building {}-bit Windows installer".format(bitness))
    if pup_pbs_url:
        os.environ["PUP_PBS_URL"] = pup_pbs_url
    cmd_sequence = (
        [sys.executable, "-m", "virtualenv", "venv-pup"],
        ["./venv-pup/Scripts/pip.exe", "install", "pup"],
        [
            "./venv-pup/Scripts/pup.exe",
            "package",
            "--launch-module=mu",
            "--nice-name=Mu Editor Custom",
            "--icon-path=./package/icons/win_icon.ico",
            "--license-path=./LICENSE",
            ".",
        ],
        ["cmd.exe", "/c", "dir", r".\dist"],
    )
    try:
        for cmd in cmd_sequence:
            print("Running:", " ".join(cmd))
            subprocess.check_call(cmd)
    finally:
        shutil.rmtree("./venv-pup", ignore_errors=True)


@export
def win32():
    """Build 32-bit Windows installer"""
    _build_windows_msi(bitness=32)


@export
def win64():
    """Build 64-bit Windows installer"""
    _build_windows_msi(bitness=64)


@export
def docs():
    """Build the docs"""
    cwd = os.getcwd()
    os.chdir("docs")
    if os.name == "nt":
        cmds = ["cmd", "/c", "make.bat", "html"]
    else:
        cmds = ["make", "html"]
    try:
        return subprocess.run(cmds).returncode
    except Exception:
        return 1
    finally:
        os.chdir(cwd)


@export
def help():
    """Display all commands with their description in alphabetical order"""
    module_doc = sys.modules["__main__"].__doc__ or "check"
    print(module_doc + "\n" + "=" * len(module_doc) + "\n")

    for command, function in sorted(_exported.items()):
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


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
