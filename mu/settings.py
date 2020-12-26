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
import platform
import sys

logger = logging.getLogger(__name__)

from . import config


class SettingsError(Exception):
    pass


class _Settings(object):
    """A _Settings object operates like a dictionary, allowing item
    access to its values. It can be loaded from and saved to a JSON
    file. Only elements which have been loaded from file and/or changed
    during the session will be written back.s

    Calling `reset` will revert to default values
    Settings `readonly` will prevent the file from being saved to disc
    `update` will update in bulk from any dict-alike structure
    """

    DEFAULTS = {}
    filename = "default.json"

    def __init__(self, **kwargs):
        self._dirty = set()
        self.filepath = "(unset)"
        print("Defaults:", self.DEFAULTS)
        self.reset()
        self.update(kwargs)
        self.readonly = False

    def __contains__(self, item):
        return item in self._dict

    def __getitem__(self, item):
        return self._dict[item]

    def __setitem__(self, item, value):
        self._dict[item] = value
        self._dirty.add(item)

    def __delitem__(self, item):
        del self._dict[item]
        self._dirty.discard(item)

    def update(self, dictalike):
        d = dict(dictalike)
        self._dict.update(d)
        self._dirty.update(d)

    def get(self, item):
        return self._dict.get(item, self.DEFAULTS.get(item))

    def __repr__(self):
        return "<%s from %s>" % (self.__class__.__name__, self.filepath)

    def reset(self):
        self._dict = dict(self.DEFAULTS)
        self._dirty.clear()

    def as_string(self, changed_only=False):
        try:
            return json.dumps(self._as_dict(changed_only), indent=2)
        except TypeError:
            logger.warn("Unable to encode settings as a string")
            raise

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

    def save(self, filepath=None):
        """Save these settings as a JSON file"""
        print("About to call save for", self)
        #
        # If this settings file is tagged readonly don't try to save it
        #
        if self.readonly:
            logger.warn("Settings is readonly; won't save")
            return

        #
        # If we don't have a filepath, bail now
        #
        saving_to_filepath = filepath or getattr(self, "filepath", None)
        if not saving_to_filepath:
            logger.warn("No filepath set; won't save")
            return

        logger.debug("Saving to %s", saving_to_filepath)
        #
        # Only save elements which have been set by the user -- either through
        # the initial file load or via actions during the application run
        #
        settings_as_string = self.as_string(changed_only=True)

        try:
            with open(saving_to_filepath, "w", encoding="utf-8") as f:
                f.write(settings_as_string)
        except Exception:
            logger.debug("Unwritten settings:\n%s", settings_as_string)
            raise

    def safely_save(self):
        try:
            self.save()
        #
        # This is an exceptional bare except as we want to shut down gracefully,
        # come what may
        #
        except Exception:
            logger.exception("Unable to save settings to %s", self.filepath)

    def register_for_autosave(self):
        atexit.register(self.safely_save)

    def quarantine_file(self, filepath):
        raise NotImplementedError

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
                    logger.exception(
                        "Unable to load settings from %s", filepath
                    )
                    json_settings = {}
                self.update(json_settings)
        except FileNotFoundError:
            logger.warn("No settings file found at %s; skipping", filepath)
        except OSError:
            logger.exception("Unable to read file at %s; skipping", filepath)

        #
        # Keep track of the filepath even if we didn't find the file: this
        # (unless overridden) is where the settings will be saved
        #
        self.filepath = filepath

    def _as_dict(self, changed_only=False):
        if changed_only:
            return dict(
                (k, v) for (k, v) in self._dict.items() if k in self._dirty
            )
        else:
            return dict(self._dict)


class _UserSettings(_Settings):

    DEFAULTS = {}
    filename = "settings.json"


class _SessionSettings(_Settings):

    DEFAULTS = {}
    filename = "session.json"


class _VirtualEnvironmentSettings(_Settings):

    DEFAULTS = {"baseline_packages": [], "dirpath": "mu_venv"}
    filename = "venv.json"


settings = _UserSettings()
session = _SessionSettings()
venv = _VirtualEnvironmentSettings()


def init(autosave=True):
    #
    # Create global singletons for the user & session settings
    # Load these from their default files and register exit
    # handlers so they are saved when the Mu process exits
    #
    # Try a number of well-known locations for the relevant
    # settings file. If it's not in any it will be "loaded" from
    # the last one in the list, causing it to be saved there at exit
    #
    # ~ settings = _UserSettings()
    # ~ for dirpath in _UserSettings.default_file_locations():
    # ~ filepath = os.path.join(dirpath, _UserSettings.filename)
    # ~ if os.path.exists(filepath):
    # ~ break
    # ~ settings.load(filepath)
    # ~ if autosave:
    # ~ settings.register_for_autosave()

    for dirpath in _SessionSettings.default_file_locations():
        filepath = os.path.join(dirpath, _SessionSettings.filename)
        if os.path.exists(filepath):
            break
    session.load(filepath)
    if autosave:
        session.register_for_autosave()

    for dirpath in _VirtualEnvironmentSettings.default_file_locations():
        filepath = os.path.join(dirpath, _VirtualEnvironmentSettings.filename)
        if os.path.exists(filepath):
            break
    venv.load(filepath)
    if autosave:
        venv.register_for_autosave()
