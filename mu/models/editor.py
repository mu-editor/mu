import os
import os.path

import sys

from mu.hybrid.repl import find_microbit

HOME_DIRECTORY = os.path.expanduser('~')
MICROPYTHON_DIRECTORY = os.path.join(HOME_DIRECTORY, 'micropython')
if not os.path.exists(MICROPYTHON_DIRECTORY):
    os.mkdir(MICROPYTHON_DIRECTORY)


class REPL:
    def __init__(self, view, port):
        self._view = view
        if os.name == 'posix':
            # If we're on Linux or OSX reference the port like this...
            self.device = "/dev/{}".format(port)
        elif os.name == 'nt':
            # On Windows do something related to an appropriate port name.
            self.device = ""
        else:
            # No idea how to deal with other OS's so fail.
            raise NotImplementedError('OS not supported :(')

    def disconnect(self):
        # Todo some teardown
        pass


class Editor:

    def __init__(self, view):
        self._view = view

        self.repl = None

    def add_repl(self):

        if self.repl is not None:
            raise RuntimeError("REPL already running")

        mb_port = find_microbit()

        if not mb_port:
            print(ResourceWarning("Could not find an attached micro:Bit"))

        view = self._view.addREPL()

        self.repl = REPL(view=view, port=mb_port)

    def remove_repl(self):

        if self.repl is None:
            raise RuntimeError("REPL not running")

        self.repl.disconnect()
        self.repl = None

    def toggle_repl(self):

        if self.repl is None:
            self.add_repl()
        else:
            self.remove_repl()

    def new(self):
        self._view.add_tab(None, '')

    def load(self):
        path = self._view.get_load_path(MICROPYTHON_DIRECTORY)

        try:
            with open(path) as f:
                text = f.read()
        except FileNotFoundError:
            pass
        else:
            self._view.add_tab(path, text)

    def save(self):
        tab = self._view.current_tab

        if tab is None:
            # There is no active text editor
            return

        if tab.path is None:
            # Unsaved file
            tab.path = self._view.get_save_path(MICROPYTHON_DIRECTORY)

        with open(tab.path, 'w') as f:
            f.write(tab.text())

        tab.modified = False

    def zoom_in(self):
        self._view.zoom_in()

    def zoom_out(self):
        self._view.zoom_out()

    def quit(self):
        """Exit the application."""
        # TODO: check for unsaved work and prompt to save if required. Fix once
        # we can actually save the work!
        sys.exit(0)
