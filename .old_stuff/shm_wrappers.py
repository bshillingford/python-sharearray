"""
Lightweight wrappers for `shm_open`. Wraps errors in exceptions. 
Returns file descriptors that can we used from e.g. `numpy` or
directly with raw `mmap`.
"""

import ctypes
from ctypes import cdll

c = cdll.LoadLibrary('libc.so.6')
rt = cdll.LoadLibrary('librt.so.1')

O_RDONLY = 0
O_WRONLY = 1
O_RDWR = 2
O_CREAT = 0o100
O_TRUNC = 0o1000


__all__ = ["open_server", "open_client", "close_server", "close_server"]


def open_server(name, size):
    """Creates and allocates shm, opens read-write."""
    fd = rt.shm_open(name, O_CREAT | O_RDWR | O_TRUNC, 0)
    if fd < 0:
        raise OSError("shm_open returned", fd, " (possibly already exists?)")
    # need ftruncate64, otherwise we can only allocate up to 2GB
    if rt.ftruncate64(fd, ctypes.c_ulong(size)) < 0:
        raise OSError("failed to allocate ", size, " bytes in new shm")
    return fd


def open_client(name, mode):
    """Opens existing shm (readonly)."""
    fd = rt.shm_open(name, O_RDONLY, 0)
    if fd < 0:
        raise OSError("shm with name " + name +
                      " not found, shm_open returned", fd)
    return fd


def close_server(fd, name):
    """Unlinks shm and closes fd."""
    rt.close(fd)
    rt.shm_unlink(name)


def close_client(fd, name):
    """Closes fd."""
    rt.close(fd)
