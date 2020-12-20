"""User and Session settings
"""

import atexit
import os
import json

from . import config


class _Settings:
    """A _Settings object operates like a dictionary, allowing item
    access to its values. It can be loaded from and saved to a JSON
    file.

    As a context manager, it saves the current state back to JSON on success
    """

    dirpath = config.DATA_DIR
    filename = "settings.json"

    def __init__(self, **kwargs):
        self._dict = dict(kwargs)

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
            os.path.join(self.dirpath, self.filename),
        )

    def save(self):
        with open(
            os.path.join(self.dirpath, self.filename), "w", encoding="utf-8"
        ) as f:
            json.dump(self._as_dict(), f)

    def reload(self, filepath):
        """Reload from a file, deliberately overwriting any existing settings

        This is intended to be used, eg, when a command-line switch overrides
        the default location
        """
        with open(
            filepath, encoding="utf-8"
        ) as f:
            self._dict = dict(json.load(f))
        self.filepath = filepath


    @classmethod
    def from_file(cls):
        with open(
            os.path.join(cls.dirpath, cls.filename), encoding="utf-8"
        ) as f:
            return cls._from_dict(json.load(f))

    @classmethod
    def _from_dict(cls, d):
        return cls(**d)

    def _as_dict(self):
        return self._dict

class _UserSettings(_Settings):

    filename = "settings.json"


class _SessionSettings(_Settings):

    filename = "session.json"


user = _UserSettings.from_file()
session = _SessionSettings.from_file()

#
# Ensure User & Session settings are saved when Python exits
#
atexit.register(user.save)
atexit.register(session.save)
