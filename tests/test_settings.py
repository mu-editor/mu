# -*- coding: utf-8 -*-

import os
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
    """Check that repr works without error
    """
    settings = mu.settings.SettingsBase()
    assert "SettingsBase" in repr(settings)

def test_as_string():
    """Check that serialisation works
    """
    settings = mu.settings.SettingsBase()
    serialised = settings.as_string()
    assert isinstance(serialised, str)

def test_as_string_unable_to_encode():
    """Check that we log an exception and raise SettingsError when
    we can't encode
    """
    settings = mu.settings.SettingsBase()
    settings['test'] = object()
    with patch.object(mu.settings, "logger") as mocked_logger:
        with pytest.raises(mu.settings.SettingsError):
            serialised = settings.as_string()

    assert mocked_logger.exception.called

def test_as_string_changed_only():
    """If serialisation is requested only with changed objects, check that
    we do that
    """
    settings = mu.settings.SettingsBase()
    unchanged_value = rstring()
    settings['unchanged'] = unchanged_value
    changed_value = rstring()
    settings['changed'] = changed_value
    settings._dirty = ("changed")

    #
    # This evidently assumes there's no encryption, compression etc. going
    # on here, but it's probably a good enough check for now
    #
    as_string = settings.as_string(changed_only=True)
    assert changed_value in as_string
    assert unchanged_value not in as_string

def test_save_readonly():
    """When a settings object is readonly save will warn and exit
    """
    settings = mu.settings.SettingsBase()
    settings.as_string = mock.Mock()
    settings.readonly = True

    with patch.object(mu.settings, "logger") as mocked_logger:
        settings.save()
    assert mocked_logger.warn.called
    assert not settings.as_string.called

def test_save_no_filepath():
    """When a settings object has no filepath save will warn and exit
    """
    settings = mu.settings.SettingsBase()
    settings.as_string = mock.Mock()
    settings.filepath = None # (just in case)

    with patch.object(mu.settings, "logger") as mocked_logger:
        settings.save()
    assert mocked_logger.warn.called
    assert not settings.as_string.called

@patch("builtins.open")
def test_save_only_changed(mocked_open):
    """When a settings object is saved only changed items are written
    """
    settings = mu.settings.SettingsBase()
    settings.filepath = rstring()
    settings.as_string = mock.Mock(return_value=rstring())
    settings.save()

    assert settings.as_string.called_with(changed_only=True)
    assert mocked_open.called_with(settings.filepath, "w")

def test_save_unable_to_write():
    """When a settings object can't be written log an exception and re-raise as
    a SettingsError
    """
    settings = mu.settings.SettingsBase()
    settings.filepath = os.curdir # this should fail on every platform

    with patch.object(mu.settings, "logger") as mocked_logger:
        with pytest.raises(mu.settings.SettingsError):
            settings.save()

    assert mocked_logger.exception.called

def test_safely_save():
    """When a settings object can't be saved, log an exception and carry on"""
    settings = mu.settings.SettingsBase()
    settings.filepath = os.curdir # this should fail on every platform
    with patch.object(mu.settings, "logger") as mocked_logger:
        settings.safely_save()

    assert mocked_logger.exception.called
