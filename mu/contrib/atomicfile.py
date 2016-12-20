# -*- coding: utf-8 -*-
import errno
import os
import sys
import tempfile
import codecs


def _get_permissions(file_path):
    """
    Get the file permissions, if it can't access them returns system default.
    """
    try:
        st_mode = os.lstat(file_path).st_mode & 0o777
    except OSError as err:
        if err.errno != errno.ENOENT:
            raise
        current_umask = os.umask(0)
        os.umask(current_umask)
        st_mode = (~current_umask) & 0o777
    return st_mode


def _make_temp(name, permissions=None):
    """
    Create a temporary file with the filename similar the given ``name``.
    The permission bits are copied from the original file or ``permissions``.

    Returns: the name of the temporary file.
    """
    d, fn = os.path.split(name)
    fd, temp_name = tempfile.mkstemp(prefix=".%s-" % fn, dir=d)
    os.close(fd)

    # Temporary files are created with mode 0600, which is usually not what we
    # want. Apply the function argument value, or copy original file mode.
    st_mode = permissions if permissions else _get_permissions(name)
    st_mode |= 0o600
    # On Windows, only the Owner Read and Write bits (0600) are affected.
    os.chmod(temp_name, st_mode)

    return temp_name


class AtomicFile(object):
    """
    Writable file object that atomically writes a file.

    All writes will go to a temporary file.
    Call ``close()`` when you are done writing, and AtomicFile will rename
    the temporary copy to the original name, making the changes visible.
    If the object is destroyed without being closed, all your writes are
    discarded.
    If an ``encoding`` argument is specified, codecs.open will be called to open
    the file in the wanted encoding.
    """
    def __init__(self, name, mode="w+b", permissions=None, encoding=None,
                 newline=None):
        self._name = name  # permanent name
        self._permissions = permissions if permissions \
            else _get_permissions(self._name)
        self._temp_name = _make_temp(name, permissions=self._permissions)
        if encoding:
            self._fp = codecs.open(self._temp_name, mode, encoding)
        else:
            if sys.version_info > (3, 0):
                self._fp = open(self._temp_name, mode, newline=newline)
            else:
                self._fp = open(self._temp_name, mode)

        # delegated methods
        self.write = self._fp.write
        self.fileno = self._fp.fileno

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type:
            return
        self.close()

    def close(self):
        if not self._fp.closed:
            self._fp.close()
            try:
                os.rename(self._temp_name, self._name)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                # Fall back to move original file and rename again
                original_to_remove = "%s.prev.bak" % self._name
                if os.path.isfile(original_to_remove):
                    # First make sure you have write access, then delete it
                    os.chmod(original_to_remove, 0o777)
                    try:
                        os.unlink(original_to_remove)
                    except OSError:
                        raise
                os.rename(self._name, original_to_remove)
                os.rename(self._temp_name, self._name)
                os.chmod(original_to_remove, 0o666)
                try:
                    os.unlink(original_to_remove)
                except OSError:
                    pass
            os.chmod(self._name, self._permissions)

    def discard(self):
        if not self._fp.closed:
            try:
                os.unlink(self._temp_name)
            except OSError:
                pass
            self._fp.close()

    def __del__(self):
        if getattr(self, "_fp", None):  # constructor actually did something
            self.discard()


def open_atomic(name, mode="w+b", permissions=None, encoding=None,
                newline=None):
    """
    Aims to be the "equivalent" of the open() function returning an
    AtomicFile object.
    """
    if 'r' in mode or 'a' in mode or 'x' in mode:
        raise TypeError('Read or append modes are not implemented.')

    if newline:
        if sys.version_info < (3, 0):
            raise TypeError("'newline' is an invalid keyword argument for this"
                            "function in Python 2.")
        if encoding:
            raise TypeError("'newline' cannot be combined with encoding")

    return AtomicFile(name, mode=mode, permissions=permissions,
                      encoding=encoding, newline=newline)
