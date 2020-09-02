# -*- coding: utf-8 -*-
"""
Tests for the Editor and REPL logic.
"""
import sys
import os
import contextlib
import shutil
import tempfile
from unittest.mock import Mock, MagicMock, patch
import uuid

import pytest
import mu.virtual_environment

@contextlib.contextmanager
def generate_tempdir(dirpath=None, delete_after=True):
    """
    Create a temp directory and populate it with on .py file, then remove it.
    """
    dirpath = dirpath or tempfile.mkdtemp(prefix="mu-")
    yield dirpath
    if delete_after:
        shutil.rmtree(dirpath)


def test_create_virtual_environment_obj():
    """Ensure a virtual environment object can be created by passing in
    a valid directory path.
    NB this doesn't create the venv itself; only the object
    """
    with generate_tempdir() as dirpath:
        venv = mu.virtual_environment.VirtualEnvironment(dirpath)
        assert venv.path == dirpath


def test_create_virtual_environment_name_obj():
    """Ensure a virtual environment object has a name.
    """
    with generate_tempdir() as dirpath:
        venv = mu.virtual_environment.VirtualEnvironment(dirpath)
        assert bool(venv.name)


def test_create_venv():
    """Ensure that we create a virtual environment.

    The nearest thing to a canonical check seems to be the presence of
    a pyvenv.cfg file
    """
    with generate_tempdir() as dirpath, \
        patch("mu.virtual_environment.VirtualEnvironment.install_baseline_packages"), \
        patch("mu.virtual_environment.VirtualEnvironment.install_jupyter_kernel"):
        venv = mu.virtual_environment.VirtualEnvironment(dirpath)
        venv.create()
        assert os.path.isfile(os.path.join(dirpath, "pyvenv.cfg"))
