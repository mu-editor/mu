# -*- coding: utf-8 -*-

import random
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
