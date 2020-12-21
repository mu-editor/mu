"""User and Session settings

User settings are common to all sessions opened by the user. Changes to this
file are likely to prevent the editor from functioning at all.

Session settings represent the latest saved state. This file can be altered
or reset and the editor will go on functioning, albeit with default options
"""

import atexit
import logging
import os
import json
import pathlib
import platform
import sys
import time

logger = logging.getLogger(__name__)

from . import config


class _Settings:
    """A _Settings object operates like a dictionary, allowing item
    access to its values. It can be loaded from and saved to a JSON
    file.

    Calling `reset` will revert to default values
    Settings `readonly` will prevent the file from being saved to disc
    `update` will update in bulk from any dict-alike structure
    """

    DEFAULTS = {}
    filename = "default.json"

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
        return "<%s from %s>" % (self.__class__.__name__, self.filepath)

    @staticmethod
    def default_file_locations():
        """
        Given an admin related filename, this function will attempt to get the
        most relevant version of this file (the default location is the application
        data directory, although a file of the same name in the same directory as
        the application itself takes preference). If this file isn't found, an
        empty one is created in the default location.

        FIXME: not sure if we still need / use this flexibility
        """
        # App location depends on being interpreted by normal Python or bundled
        app_path = (
            sys.executable if getattr(sys, "frozen", False) else sys.argv[0]
        )
        app_dir = os.path.dirname(os.path.abspath(app_path))
        # The os x bundled application is placed 3 levels deep in the .app folder
        if platform.system() == "Darwin" and getattr(sys, "frozen", False):
            app_dir = os.path.dirname(
                os.path.dirname(os.path.dirname(app_dir))
            )

        return [app_dir, config.DATA_DIR]

    def save(self):
        if self.readonly:
            logger.warn("Settings is readonly; won't save")
        else:
            logger.debug("Saving to %s", self.filepath)
            with open(self.filepath, "w", encoding="utf-8") as f:
                try:
                    json.dump(self._as_dict(), f, indent=2)
                except TypeError:
                    #
                    # Quarantine the file to avoid problems starting up next time
                    # (Close it first or we won't be able to rename on Windows)
                    #
                    f.close()
                    quarantined_filename = "FAILED-%s.json" % time.strftime("%Y%m%d%H%M%S")
                    quarantined_dirpath = os.path.dirname(self.filepath)
                    os.rename(self.filepath, os.path.join(quarantined_dirpath, quarantined_filename))
                    logger.exception("Unable to save settings to %s; quarantined file as %s", self.filepath, quarantined_filename)

    def load(self, filepath):
        """Load from a file, merging into existing settings

        This is intended to be used, eg, when a command-line switch overrides
        the default location. It'll probably be preceded by a call to `reset`.

        But it could be used to implement a cascade of settings, eg for an
        admin to set site-wide settings followed by user settings. This might
        be implemented by, eg, command-line switches specifying more than one
        settings file. If this happens, the last file named becomes the settings's
        filepath -- meaning that's where the settings will be saved at the end
        of the session.

        This operates in a similar way to configparser: if a file isn't found
        the function silently succeeds. However the filepath is still stored.
        This has the effect that, eg, loading a site-wide admin file first
        followed by a user-specific file will load the admin settings, but will
        save to the user-specific file.
        """
        try:
            with open(filepath, encoding="utf-8") as f:
                try:
                    json_settings = json.load(f)
                except json.decoder.JSONDecodeError:
                    logger.exception("Unable to load settings from %s", filepath)
                    json_settings = {}
                self.update(json_settings)
        except FileNotFoundError:
            logger.warn("No settings file found at %s; skipping", filepath)

        #
        # Keep track of the filepath even if we didn't find the file: this
        # (unless overridden) is where the settings will be saved
        #
        self.filepath = filepath

    def reset(self):
        self._dict = dict(self.DEFAULTS)

    def _as_dict(self):
        return self._dict


class _UserSettings(_Settings):

    DEFAULTS = {}
    filename = "settings.json"


class _SessionSettings(_Settings):

    DEFAULTS = {}
    filename = "session.json"


#
# Create global singletons for the user & session settings
# Load these from their default files and register exit
# handlers so they are saved when the Mu process exits
#
# Try a number of well-known locations for the relevant
# settings file. If it's not in any it will be "loaded" from
# the last one in the list, causing it to be saved there at exit
#
user = _UserSettings()
for dirpath in _UserSettings.default_file_locations():
    filepath = os.path.join(dirpath, _UserSettings.filename)
    if os.path.exists(filepath):
        break
user.load(filepath)
atexit.register(user.save)

session = _SessionSettings()
for dirpath in _SessionSettings.default_file_locations():
    filepath = os.path.join(dirpath, _SessionSettings.filename)
    if os.path.exists(filepath):
        break
session.load(filepath)
atexit.register(session.save)
