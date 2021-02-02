"""
The Web mode for the Mu editor, using Flask.

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
import webbrowser
import signal
from mu.modes.base import BaseMode
from mu.modes.api import PYTHON3_APIS, SHARED_APIS, FLASK_APIS
from mu.resources import load_icon
from mu.logic import read_and_decode
from ..virtual_environment import venv


logger = logging.getLogger(__name__)


MUWEB_TEMPLATE = """# Wraps the user's Flask application with boilerplate.
from {} import app


app.run()
"""


CODE_TEMPLATE = """# A simple web application.
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')
"""


class WebMode(BaseMode):
    """
    Represents the functionality required by the WWW mode.
    """

    name = _("Web")
    short_name = "web"
    description = _('Build simple websites with the "Flask" web framework.')
    icon = "web"
    runner = None
    save_timeout = 0  # User has to explicitly save web application.
    file_extensions = ["css", "html"]
    code_template = CODE_TEMPLATE

    def actions(self):
        """
        Return an ordered list of actions provided by this module. An action
        is a name (also used to identify the icon) , description, and handler.
        """
        return [
            {
                "name": "run",
                "display_name": _("Run"),
                "description": _("Run the web server."),
                "handler": self.run_toggle,
                "shortcut": "F5",
            },
            {
                "name": "browse",
                "display_name": _("Browse"),
                "description": _("Open your website in a browser."),
                "handler": self.browse,
                "shortcut": "Ctrl+Shift+B",
            },
            {
                "name": "templates",
                "display_name": _("Templates"),
                "description": _("Load HTML templates used by your website."),
                "handler": self.load_templates,
                "shortcut": "Ctrl+Shift+T",
            },
            {
                "name": "css",
                "display_name": _("CSS"),
                "description": _("Load CSS files used by your website."),
                "handler": self.load_css,
                "shortcut": "Ctrl+Shift+C",
            },
            {
                "name": "static",
                "display_name": _("Images"),
                "description": _(
                    "Open the directory containing images used "
                    "by your website."
                ),
                "handler": self.show_images,
                "shortcut": "Ctrl+Shift+I",
            },
        ]

    def api(self):
        """
        Return a list of API specifications to be used by auto-suggest and call
        tips.
        """
        return SHARED_APIS + PYTHON3_APIS + FLASK_APIS

    def run_toggle(self, event):
        """
        Handles the toggling of the run button to start/stop the server.
        """
        if self.runner:
            self.stop_server()
            run_slot = self.view.button_bar.slots["run"]
            run_slot.setIcon(load_icon("run"))
            run_slot.setText(_("Run"))
            run_slot.setToolTip(_("Run the web server."))
            self.set_buttons(modes=True)
        else:
            self.start_server()
            if self.runner:
                run_slot = self.view.button_bar.slots["run"]
                run_slot.setIcon(load_icon("stop"))
                run_slot.setText(_("Stop"))
                run_slot.setToolTip(_("Stop the web server."))
                self.set_buttons(modes=False)

    def start_server(self):
        """
        Run the current file as a webserver.
        """
        # Grab the Python file.
        tab = self.view.current_tab
        if tab is None:
            logger.debug("There is no active text editor.")
            self.stop_server()
            return
        if tab.path is None:
            # Unsaved file.
            self.editor.save()
        if tab.path:
            # Check it's a Python file.
            if not tab.path.lower().endswith(".py"):
                # Oops... show a helpful message and stop.
                msg = _("This is not a Python file!")
                info = _(
                    "Mu is only able to serve a Python file. Please make "
                    "sure the current tab in Mu is the one for your web "
                    "application and then try again."
                )
                self.view.show_message(msg, info)
                self.stop_server()
                return
            # If needed, save the script.
            if tab.isModified():
                self.editor.save_tab_to_file(tab)
            logger.debug(tab.text())
            envars = self.editor.envars
            envars.append(("FLASK_APP", os.path.basename(tab.path)))
            envars.append(("FLASK_ENV", "development"))
            envars.append(("LC_ALL", "en_GB.UTF8"))
            envars.append(("LANG", "en_GB.UTF8"))
            args = ["-m", "flask", "run"]
            cwd = os.path.dirname(tab.path)
            self.runner = self.view.add_python3_runner(
                venv.interpreter,
                "",
                cwd,
                interactive=False,
                envars=envars,
                python_args=args,
            )
            logger.debug("Starting Flask app.")
            self.runner.process.waitForStarted()

    def stop_server(self):
        """
        Stop the currently running web server.
        """
        logger.debug("Stopping Flask app.")
        if self.runner:
            try:
                pid = self.runner.process.processId()
                os.kill(pid, signal.SIGINT)
            except Exception as ex:
                # Couldn't kill child process. Perhaps it's already finished
                # because it encountered an error. In any case, log this for
                # debugging purposes.
                logger.error("Problem stopping local web server.")
                logger.error(ex)
            self.runner.process.waitForFinished()
            self.runner = None
        self.view.remove_python_runner()

    def stop(self):
        """
        Called by logic.quit, so if the server is running, stop it.
        """
        self.stop_server()

    def open_file(self, path):
        """
        Open the referenced file (html / css).
        """
        return read_and_decode(path)

    def load_templates(self, event):
        """
        Open the directory containing the HTML template views used by Flask.

        This should open the host OS's file system explorer so users can drag
        new files into the opened folder.
        """
        templates_dir = self.assets_dir("templates")
        logger.info(templates_dir)
        self.editor.load(default_path=templates_dir)

    def load_css(self, event):
        """
        Open the directory containing the HTML template views used by Flask.

        This should open the host OS's file system explorer so users can drag
        new files into the opened folder.
        """
        css_path = os.path.join("static", "css")
        css_dir = self.assets_dir(css_path)
        logger.info(css_dir)
        self.editor.load(default_path=css_dir)

    def show_images(self, event):
        """
        Open the directory containing the static image assets used by Flask.

        This should open the host OS's file system explorer so users can drag
        new files into the opened folder.
        """
        img_path = os.path.join("static", "img")
        img_dir = self.assets_dir(img_path)
        logger.info(img_dir)
        self.view.open_directory_from_os(img_dir)

    def browse(self, event):
        """
        Open the default browser to http://127.0.0.1:5080/ if the local web
        server is running, otherwise display a helpful message.
        """
        if self.runner:
            url = "http://127.0.0.1:5000/"
            logger.info("Opening local website at: {}".format(url))
            webbrowser.open(url)
        else:
            logger.info("Attempted to load website, but server not running.")
            msg = _("Cannot Open Website - Server not Running.")
            info = _(
                "You must have the local web server running in order to "
                "view your website in a browser. Click on the 'Run' "
                "button to start the server and then try again."
            )
            self.view.show_message(msg, info)
