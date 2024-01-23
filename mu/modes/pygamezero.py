"""
The Pygame Zero mode for the Mu editor.

Copyright (c) 2015-2017 Nicholas H.Tollervey and others (see the AUTHORS file).

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import logging
from mu.modes.base import BaseMode
from mu.modes.api import PYTHON3_APIS, SHARED_APIS, PI_APIS, PYGAMEZERO_APIS, NEOPIA_APIS
from mu.resources import load_icon
from ..virtual_environment import venv
import re


logger = logging.getLogger(__name__)


class PyGameZeroMode(BaseMode):
    """
    Represents the functionality required by the PyGameZero mode.
    """

    name = _("Pygame Zero")
    short_name = "pygamezero"
    description = _("Make games with Pygame Zero.")
    icon = "pygamezero"
    runner = None
    builtins = [
        "clock",
        "music",
        "Actor",
        "keyboard",
        "animate",
        "Rect",
        "ZRect",
        "images",
        "sounds",
        "mouse",
        "keys",
        "keymods",
        "exit",
        "screen",
    ]

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        return [
            {
                "name": "play",
                "display_name": _("Play"),
                "description": _("Play your Pygame Zero game."),
                "handler": self.play_toggle,
                "shortcut": "F5",
            },
            {
                "name": "images",
                "display_name": _("Images"),
                "description": _("Show the images used by Pygame Zero."),
                "handler": self.show_images,
                "shortcut": "Ctrl+Shift+I",
            },
            {
                "name": "fonts",
                "display_name": _("Fonts"),
                "description": _("Show the fonts used by Pygame Zero."),
                "handler": self.show_fonts,
                "shortcut": "Ctrl+Shift+F",
            },
            {
                "name": "sounds",
                "display_name": _("Sounds"),
                "description": _("Show the sounds used by Pygame Zero."),
                "handler": self.show_sounds,
                "shortcut": "Ctrl+Shift+N",
            },
            {
                "name": "music",
                "display_name": _("Music"),
                "description": _("Show the music used by Pygame Zero."),
                "handler": self.show_music,
                "shortcut": "Ctrl+Shift+M",
            },
            {
                "name": "package",
                "display_name": _("Package"),
                "description": _("Package the game to one-file for distribution."),
                "handler": self.toggle_package,
                "shortcut": "F6",
            },
        ]

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS + PYTHON3_APIS + PI_APIS + PYGAMEZERO_APIS + NEOPIA_APIS

    def play_toggle(self, event):
        """
        Handles the toggling of the play button to start/stop a script.
        """
        if self.runner:
            self.stop_game()
            play_slot = self.view.button_bar.slots["play"]
            play_slot.setIcon(load_icon("play"))
            play_slot.setText(_("Play"))
            play_slot.setToolTip(_("Play your Pygame Zero game."))
            self.set_buttons(modes=True)
        else:
            self.run_game()
            if self.runner:
                play_slot = self.view.button_bar.slots["play"]
                play_slot.setIcon(load_icon("stop"))
                play_slot.setText(_("Stop"))
                play_slot.setToolTip(_("Stop your Pygame Zero game."))
                self.set_buttons(modes=False)

    def run_game(self):
        """
        Run the current game.
        """
        # Grab the Python file.
        tab = self.view.current_tab
        if tab is None:
            logger.debug("There is no active text editor.")
            self.stop_game()
            return
        if tab.path is None:
            # Unsaved file.
            self.editor.save()
        if tab.path:
            # If needed, save the script.
            if tab.isModified():
                self.editor.save_tab_to_file(tab)
            logger.debug(tab.text())
            envars = self.editor.envars
            args = ["-m", "pgzero"]
            cwd = os.path.dirname(tab.path)

            self.runner = self.view.add_python3_runner(
                interpreter=venv.interpreter,
                script_name=tab.path,
                working_directory=cwd,
                interactive=False,
                envars=envars,
                python_args=args,
            )
            self.runner.process.waitForStarted()

    def stop_game(self):
        """
        Stop the currently running game.
        """
        logger.debug("Stopping script.")
        if self.runner:
            self.runner.stop_process()
            self.runner = None
        self.view.remove_python_runner()

    def show_images(self, event):
        """
        Open the directory containing the image assets used by Pygame Zero.

        This should open the host OS's file system explorer so users can drag
        new files into the opened folder.
        """
        self.view.open_directory_from_os(self.assets_dir("images"))

    def show_fonts(self, event):
        """
        Open the directory containing the font assets used by Pygame Zero.

        This should open the host OS's file system explorer so users can drag
        new files into the opened folder.
        """
        self.view.open_directory_from_os(self.assets_dir("fonts"))

    def show_sounds(self, event):
        """
        Open the directory containing the sound assets used by Pygame Zero.

        This should open the host OS's file system explorer so users can drag
        new files into the opened folder.
        """
        self.view.open_directory_from_os(self.assets_dir("sounds"))

    def show_music(self, event):
        """
        Open the directory containing the music assets used by Pygame Zero.

        This should open the host OS's file system explorer so users can drag
        new files into the opened folder.
        """
        self.view.open_directory_from_os(self.assets_dir("music"))

    def toggle_package(self, event):
        """
        Handles the toggling of the package button to start/stop a packaging.
        """
        if self.runner:
            self.stop_game()
            package_slot = self.view.button_bar.slots["package"]
            package_slot.setIcon(load_icon("package"))
            package_slot.setText(_("package"))
            package_slot.setToolTip(_("Package the game to one-file for distribution."))
            self.set_buttons(modes=True)
        else:
            self.run_package()
            if self.runner:
                package_slot = self.view.button_bar.slots["package"]
                package_slot.setIcon(load_icon("stop"))
                package_slot.setText(_("Stop"))
                package_slot.setToolTip(_("Stop packaging your Pygame Zero game."))
                self.set_buttons(modes=False)

    def run_package(self):
        """
        Package the game to one-file for distribution.
        """
         # Grab the Python file.
        tab = self.view.current_tab
        if tab is None:
            logger.debug("There is no active text editor.")
            self.stop_game()
            return
        if tab.path is None:
            # Unsaved file.
            self.editor.save()
        if tab.path:
            # If needed, save the script.
            if tab.isModified():
                self.editor.save_tab_to_file(tab)
            logger.debug(tab.text())

            # Tidy source code to find error earlier
            try:
                self.editor.tidy_code()
            except Exception:
                logger.debug("Failed in tiding code")
                return

            # Add pgzrun to the source
            source_code = tab.text()
            source_code = "import pgzrun\n" + source_code
            source_code += "\npgzrun.go()"
            tab.SendScintilla(tab.SCI_SETTEXT, source_code.encode("utf-8"))

            # Make agrs
            cwd = os.path.dirname(tab.path)
            envars = self.editor.envars
            cmd_args = ["--collect-all", "pgzero", "--onefile", "--clean"]
            img_dir = os.path.join(cwd, "images")
            if os.path.isdir(img_dir) and len(os.listdir(img_dir)) != 0:
                cmd_args += ["--add-data", "images/*:images"]
            font_dir = os.path.join(cwd, "fonts")
            if os.path.isdir(font_dir) and len(os.listdir(font_dir)) != 0:
                cmd_args += ["--add-data", "fonts/*:fonts"]
            sound_dir = os.path.join(cwd, "sounds")
            if os.path.isdir(sound_dir) and len(os.listdir(sound_dir)) != 0:
                cmd_args += ["--add-data", "sounds/*:sounds"]
            music_dir = os.path.join(cwd, "music")
            if os.path.isdir(music_dir) and len(os.listdir(music_dir)) != 0:
                cmd_args += ["--add-data", "music/*:music"]
            args = ["-m", "PyInstaller"]
            self.runner = self.view.add_python3_runner(
                interpreter=venv.interpreter,
                script_name=tab.path,
                working_directory=cwd,
                interactive=False,
                envars=envars,
                python_args=args,
                command_args=cmd_args
            )
            self.runner.process.waitForStarted()
            self.runner.process.finished.connect(self.finished)

    def finished(self):
        """
        Remove pgzrun from the source when the packaging process is finished
        """
        tab = self.view.current_tab
        source_code = tab.text()
        source_code = re.sub(r"import pgzrun\n", "", source_code, flags = re.DOTALL)
        source_code = re.sub(r"\npgzrun\.go\(\)", "", source_code, flags = re.DOTALL)
        tab.SendScintilla(tab.SCI_SETTEXT, source_code.encode("utf-8"))
