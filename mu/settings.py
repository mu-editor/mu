"""User and Session settings

User settings are common to all sessions opened by the user. Changes to this
file are likely to prevent the editor from functioning at all.

Session settings represent the latest saved state. This file can be altered
or reset and the editor will go on functioning, albeit with default options
"""

import atexit
import os
import json

from . import config


class _Settings:
    """A _Settings object operates like a dictionary, allowing item
    access to its values. It can be loaded from and saved to a JSON
    file.
    """

    DEFAULTS = {}

    def __init__(self, **kwargs):
        self.reset()
        self.update(kwargs)
        self.readonly = False

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, item, value):
        self._dict[item] = value

    def __delitem__(self, item):
        del self._dict[item]

    def update(self, dictalike):
        self._dict.update(dictalike)

    def __repr__(self):
        return "<%s from %s>" % (
            self.__class__.__name__,
            self.filepath
        )

    def save(self):
        if not self.readonly:
            with open(
                self.filepath, "w", encoding="utf-8"
            ) as f:
                json.dump(self._as_dict(), f)

    def load(self, filepath):
        """Reload from a file, merging into existing settings

        This is intended to be used, eg, when a command-line switch overrides
        the default location
        """
        with open(
            filepath, encoding="utf-8"
        ) as f:
            self.update(json.load(f))
        self.filepath = filepath

    def reset(self):
        self._dict = dict(self.DEFAULTS)

    def _as_dict(self):
        return self._dict

class _UserSettings(_Settings):

    DEFAULTS = {}


class _SessionSettings(_Settings):

    DEFAULTS = {}


user = _UserSettings()
user.load(os.path.join(config.DATA_DIR, "settings.json"))
atexit.register(user.save)

session = _SessionSettings()
session.load(os.path.join(config.DATA_DIR, "session.json"))
atexit.register(session.save)
