# -*- coding: utf-8 -*-
"""
Tests for the Editor and REPL logic.
"""
import sys
import os
import contextlib
import shutil
import tempfile
import uuid

import pytest
import mu.virtual_environment

@contextlib.contextmanager
def generate_tempdir(dirpath=None):
    """
    Create a temp directory and populate it with on .py file, then remove it.
    """
    dirpath = dirpath or tempfile.mkdtemp(prefix="mu-")
    yield dirpath
    shutil.rmtree(dirpath)


def test_create_virtual_environment():
    """Ensure a virtual environment object can be created by passing in
    a valid directory path.
    NB this doesn't create the venv itself; only the object
    """
    with generate_tempdir() as dirpath:
        venv = mu.virtual_environment.VirtualEnvironment(dirpath)
        assert venv.path == dirpath


def test_create_virtual_environment_name():
    """Ensure a virtual environment object has a name.
    """
    with generate_tempdir() as dirpath:
        venv = mu.virtual_environment.VirtualEnvironment(dirpath)
        assert bool(venv.name)

