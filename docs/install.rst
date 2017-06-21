Installation
============

Currently, the latest builds for Windows, OSX and Linux x86 can be found here:

http://mu-builds.s3-website.eu-west-2.amazonaws.com

Go to the link above, choose the directory for your platform and download the
latest build of the editor.

.. note::

    There will be several versions of the editor for each platform. They're
    ordered by date, so choose the latest version.

Windows
-------

Download the ``.exe`` file and double click it to launch.

Once you've got past the Windows induced warnings and privilege requests you'll
see the editor.

.. warning::

    To use the editor's interactive programming feature (the REPL) with a BBC
    micro:bit you'll need to install a driver for USB/serial connectivity. You
    can find the driver and details instructions for installing it on
    `ARM's website <https://developer.mbed.org/handbook/Windows-serial-configuration>`_. We're trying to find a way around this via Windows packaging.

OSX
---

Download the latest build and double-click it to run. OSX will probably ask you
to confirm you want to run a program downloaded from the internet. You may need
to right-click on the file and select `open` to make it work first time. You do
not need to install any drivers.

Linux
-----

Download the latest build and make it executable::

    chmod +x mu.bin

Run it from the command line like this::

    ./mu.bin

Or double-click it in your file-manager.

We're in the process of creating official packages for both Debian and Fedora
based flavours (including Raspbian for the Raspberry Pi). In both cases you'll
be able to use the built-in package manager and Mu will appear as a regular
application.
