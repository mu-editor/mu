# -*- coding: utf-8 -*-

import os
import sys
import random
from unittest import mock
from unittest.mock import patch

import pytest

import mu.settings


def rstring(length=10, characters="abcdefghijklmnopqrstuvwxyz"):
    letters = list(characters)
    random.shuffle(letters)
    return "".join(letters[:length])


def test_creation():
    """We should be able to create a new SettingsBase object without error"""
    s = mu.settings.SettingsBase()
    assert s is not None


def test_creation_with_keywords():
    """Keyword args passed in to the SettingsBase constructor should appear
    as setting items
    """
    k1, v1 = rstring(), rstring()
    k2, v2 = rstring(), rstring()
    keywords = {k1: v1, k2: v2}
    s = mu.settings.SettingsBase(**keywords)
    assert s[k1] == v1
    assert s[k2] == v2


def test_keywords_are_changed():
    """Keyword args should should be considered changed for the purposes
    of saving
    """
    k1, v1 = rstring(), rstring()
    keywords = {k1: v1}
    s = mu.settings.SettingsBase(**keywords)
    assert k1 in s._dirty


def test_getitem():
    """A settings item should be accessible as value = settings[item]"""
    k1, v1 = rstring(), rstring()
    s = mu.settings.SettingsBase(**{k1: v1})
    assert s[k1] == v1


def test_setitem():
    """A settings item should be set by settings[item] = value"""
    k1, v1 = rstring(), rstring()
    s = mu.settings.SettingsBase()
    s[k1] = v1
    assert s[k1] == v1


def test_setitem_is_changed():
    """Items updated by setitem are tagged as changes"""
    k1, v1 = rstring(), rstring()
    s = mu.settings.SettingsBase()
    s[k1] = v1
    assert k1 in s._dirty


def test_delitem():
    """A settings item should be removed by del settings[item]"""
    k1, v1 = rstring(), rstring()
    s = mu.settings.SettingsBase(**{k1: v1})
    del s[k1]
    with pytest.raises(KeyError):
        s[k1]


def test_delitem_is_not_changed():
    """Items removed by delitem should not be tagged as changes"""
    k1, v1 = rstring(), rstring()
    s = mu.settings.SettingsBase(**{k1: v1})
    del s[k1]
    assert k1 not in s._dirty


def test_update():
    """Items can by added en bloc by update"""
    k1, v1 = rstring(), rstring()
    s = mu.settings.SettingsBase(**{k1: v1})
    k2, v2 = rstring(), rstring()
    k3, v3 = rstring(), rstring()
    d = {k2: v2, k3: v3}
    s.update(d)

    assert s[k2] == v2
    assert s[k3] == v3


def test_update_is_changed():
    """Items added by update are tagged as changes"""
    k1, v1 = rstring(), rstring()
    s = mu.settings.SettingsBase(**{k1: v1})
    k2, v2 = rstring(), rstring()
    k3, v3 = rstring(), rstring()
    d = {k2: v2, k3: v3}
    s.update(d)

    assert k2 in s._dirty
    assert k3 in s._dirty


def test_get_item_exists():
    """Get when the item exists returns its value"""
    k1, v1 = rstring(), rstring()
    s = mu.settings.SettingsBase(**{k1: v1})
    assert s.get(k1) == v1


def test_get_return_default():
    """Get when the item does not exist returns the default"""
    k1, v1 = rstring(), rstring()
    with patch.object(mu.settings.SettingsBase, "DEFAULTS", {k1: v1}):
        s = mu.settings.SettingsBase()
        #
        # Settings are populated with their defaults. So remove
        # k1 before going ahead
        #
        del s[k1]
        assert k1 not in s
        assert s.get(k1) == v1


def test_get_return_none():
    """Get when the item does not exist and has no default return None"""
    k1 = rstring()
    s = mu.settings.SettingsBase()
    assert s.get(k1) is None


def test_reset_has_defaults():
    """When reset revert to defaults"""
    k1, v1 = rstring(), rstring()
    defaults = {k1: v1}
    with patch.object(mu.settings.SettingsBase, "DEFAULTS", defaults):
        s = mu.settings.SettingsBase()
        k2, v2 = rstring(), rstring()
        s[k2] = v2

        assert s._as_dict() != defaults
        s.reset()
        assert s._as_dict() == defaults


def test_reset_nothing_changed():
    """When reset nothing is tagged as changes"""
    k1, v1 = rstring(), rstring()
    defaults = {k1: v1}
    with patch.object(mu.settings.SettingsBase, "DEFAULTS", defaults):
        s = mu.settings.SettingsBase()
        k2, v2 = rstring(), rstring()
        s[k2] = v2
        assert s._dirty
        s.reset()
        assert not s._dirty


def test_repr():
    """Check that repr works without error"""
    settings = mu.settings.SettingsBase()
    assert "SettingsBase" in repr(settings)


def test_as_string():
    """Check that serialisation works"""
    settings = mu.settings.SettingsBase()
    serialised = settings.as_string()
    assert isinstance(serialised, str)


@patch.object(mu.settings, "logger")
def test_as_string_unable_to_encode(mocked_logger):
    """Check that we log an exception and raise SettingsError when
    we can't encode
    """
    settings = mu.settings.SettingsBase()
    settings["test"] = object()
    with pytest.raises(mu.settings.SettingsError):
        _ = settings.as_string()

    assert mocked_logger.exception.called


def test_as_string_changed_only():
    """If serialisation is requested only with changed objects, check that
    we do that
    """
    settings = mu.settings.SettingsBase()
    unchanged_value = rstring()
    settings["unchanged"] = unchanged_value
    changed_value = rstring()
    settings["changed"] = changed_value
    settings._dirty = "changed"

    #
    # This evidently assumes there's no encryption, compression etc. going
    # on here, but it's probably a good enough check for now
    #
    as_string = settings.as_string(changed_only=True)
    assert changed_value in as_string
    assert unchanged_value not in as_string


@patch.object(mu.settings, "logger")
def test_save_readonly(mocked_logger):
    """When a settings object is readonly save will warn and exit"""
    settings = mu.settings.SettingsBase()
    settings.as_string = mock.Mock()
    settings.readonly = True

    settings.save()
    assert mocked_logger.warn.called
    assert not settings.as_string.called


@patch.object(mu.settings, "logger")
def test_save_no_filepath(mocked_logger):
    """When a settings object has no filepath save will warn and exit"""
    settings = mu.settings.SettingsBase()
    settings.as_string = mock.Mock()
    settings.filepath = None  # (just in case)

    settings.save()
    assert mocked_logger.warn.called
    assert not settings.as_string.called


@patch("builtins.open")
def test_save_only_changed(mocked_open):
    """When a settings object is saved only changed items are written"""
    settings = mu.settings.SettingsBase()
    settings.filepath = rstring()
    settings.as_string = mock.Mock(return_value=rstring())
    settings.save()

    assert settings.as_string.called_with(changed_only=True)
    assert mocked_open.called_with(settings.filepath, "w")


@patch.object(mu.settings, "logger")
def test_save_unable_to_write(mocked_logger):
    """When a settings object can't be written log an exception"""
    settings = mu.settings.SettingsBase()
    settings.filepath = os.curdir  # this should fail on every platform
    settings.save()

    assert mocked_logger.exception.called


@patch("builtins.open")
@patch.object(mu.settings, "logger")
def test_save_unable_to_encode(mocked_logger, mocked_open):
    """When a settings object can't be written log an exception and exit"""
    settings = mu.settings.SettingsBase()
    settings.filepath = rstring()
    settings[rstring()] = object()
    settings.save()

    assert not mocked_open.called
    assert mocked_logger.exception.called


@patch.object(mu.settings, "logger")
def test_load_file_not_found(mocked_logger):
    """When a settings object can't be found log a warning and carry on with that
    filepath held for later
    """
    filepath = rstring()
    assert not os.path.exists(filepath), (
        "Unexpectedly, %s actually exists!" % filepath
    )
    settings = mu.settings.SettingsBase()
    settings.load(filepath)

    assert mocked_logger.warn.called
    assert settings.filepath == filepath


@patch.object(mu.settings, "logger")
def test_load_file_unable_to_read(mocked_logger):
    """When a settings object can't be read log an exception and carry on with that
    filepath held for later
    """
    filepath = os.curdir  # certain to fail on every platform
    settings = mu.settings.SettingsBase()
    settings.load(filepath)

    assert mocked_logger.exception.called
    assert settings.filepath == filepath


def test_expandvars_string():
    """When a string value contains an embedded environment variable it is
    expanded to its underlying value
    """
    key, envvar_name, value = rstring(), rstring(), rstring()
    if sys.platform == "win32":
        envvar = "%{}%".format(envvar_name)
    else:
        envvar = "${}".format(envvar_name)
    os.environ[envvar_name] = value
    s = mu.settings.SettingsBase()
    s[key] = envvar

    assert s[key] == value


def test_expandvars_none():
    """When a value is None the expand mechanism does not fail"""
    key = rstring()
    s = mu.settings.SettingsBase()
    s[key] = None

    assert s[key] is None


def test_expandvars_nonexistent_envvar():
    """When a value refers to an envvar which does not exist, follow the
    conventional approach of returning the envvar name unaltered

    ie if we have "%NON-EXISTENT%\abc" then the value returned will
    be "%NON-EXISTENT%\abc"
    """
    key, envvar_name = rstring(), rstring()
    if sys.platform == "win32":
        envvar = "%{}%".format(envvar_name)
    else:
        envvar = "${}".format(envvar_name)
    s = mu.settings.SettingsBase()
    s[key] = envvar

    assert s[key] == envvar

def test_get_admin_file_path():
    """
    Finds an admin file in the application location, when Mu is run as if
    NOT frozen by PyInstaller.
    """
    fake_app_path = os.path.dirname(__file__)
    fake_app_script = os.path.join(fake_app_path, "run.py")
    wrong_fake_path = "wrong/path/to/executable"
    fake_local_settings = os.path.join(fake_app_path, "settings.json")
    with mock.patch.object(
        sys, "executable", wrong_fake_path
    ), mock.patch.object(sys, "argv", [fake_app_script]):
        result = mu.logic.get_admin_file_path("settings.json")
        assert result == fake_local_settings


def test_get_admin_file_path_frozen():
    """
    Find an admin file in the application location when it has been frozen
    using PyInstaller.
    """
    fake_app_path = os.path.dirname(__file__)
    fake_app_script = os.path.join(fake_app_path, "mu.exe")
    wrong_fake_path = "wrong/path/to/executable"
    fake_local_settings = os.path.join(fake_app_path, "settings.json")
    with mock.patch.object(
        sys, "frozen", create=True, return_value=True
    ), mock.patch(
        "platform.system", return_value="not_Darwin"
    ), mock.patch.object(
        sys, "executable", fake_app_script
    ), mock.patch.object(
        sys, "argv", [wrong_fake_path]
    ):
        result = mu.logic.get_admin_file_path("settings.json")
        assert result == fake_local_settings


def test_get_admin_file_path_frozen_osx():
    """
    Find an admin file in the application location when it has been frozen
    using PyInstaller on macOS (as the path is different in the app bundle).
    """
    fake_app_path = os.path.join(os.path.dirname(__file__), "a", "b", "c")
    fake_app_script = os.path.join(fake_app_path, "mu.exe")
    wrong_fake_path = "wrong/path/to/executable"
    fake_local_settings = os.path.abspath(
        os.path.join(fake_app_path, "..", "..", "..", "settings.json")
    )
    with mock.patch.object(
        sys, "frozen", create=True, return_value=True
    ), mock.patch("platform.system", return_value="Darwin"), mock.patch.object(
        sys, "executable", fake_app_script
    ), mock.patch.object(
        sys, "argv", [wrong_fake_path]
    ):
        result = mu.logic.get_admin_file_path("settings.json")
        assert result == fake_local_settings


def test_get_admin_file_path_with_data_path():
    """
    Find an admin file in the data location.
    """
    mock_open = mock.mock_open()
    mock_exists = mock.MagicMock()
    mock_exists.side_effect = [False, True]
    mock_json_dump = mock.MagicMock()
    with mock.patch("os.path.exists", mock_exists), mock.patch(
        "builtins.open", mock_open
    ), mock.patch("json.dump", mock_json_dump), mock.patch(
        "mu.logic.DATA_DIR", "fake_path"
    ):
        result = mu.logic.get_admin_file_path("settings.json")
        assert result == os.path.join("fake_path", "settings.json")
    assert not mock_json_dump.called


def test_get_admin_file_path_no_files():
    """
    No admin file found, so create one.
    """
    mock_open = mock.mock_open()
    mock_json_dump = mock.MagicMock()
    with mock.patch("os.path.exists", return_value=False), mock.patch(
        "builtins.open", mock_open
    ), mock.patch("json.dump", mock_json_dump), mock.patch(
        "mu.logic.DATA_DIR", "fake_path"
    ):
        result = mu.logic.get_admin_file_path("settings.json")
        assert result == os.path.join("fake_path", "settings.json")
    assert mock_json_dump.call_count == 1


def test_get_admin_file_path_no_files_cannot_create():
    """
    No admin file found, attempting to create one causes Mu to log and
    make do.
    """
    mock_open = mock.MagicMock()
    mock_open.return_value.__enter__.side_effect = FileNotFoundError("Bang")
    mock_open.return_value.__exit__ = mock.Mock()
    mock_json_dump = mock.MagicMock()
    with mock.patch("os.path.exists", return_value=False), mock.patch(
        "builtins.open", mock_open
    ), mock.patch("json.dump", mock_json_dump), mock.patch(
        "mu.logic.DATA_DIR", "fake_path"
    ), mock.patch(
        "mu.logic.logger", return_value=None
    ) as logger:
        mu.logic.get_admin_file_path("settings.json")
        msg = (
            "Unable to create admin file: "
            "fake_path{}settings.json".format(os.path.sep)
        )
        logger.error.assert_called_once_with(msg)

