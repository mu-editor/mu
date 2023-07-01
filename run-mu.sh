#!/bin/sh
export WAYLAND_DISPLAY=wayland-0
#~ export XDG_RUNTIME_DIR=/tmp/1000-runtime-dir
#export QT_QPA_PLATFORM=wayland
export WAYLAND_DEBUG=1
export PYTHONDEVMODE=1
dist/Mu_Editor-1.2.1-x86_64.AppImage
