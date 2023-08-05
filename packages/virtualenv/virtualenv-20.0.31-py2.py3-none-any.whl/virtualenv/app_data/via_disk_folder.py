# -*- coding: utf-8 -*-
"""
A rough layout of the current storage goes as:

virtualenv-app-data
├── py - <version> <cache information about python interpreters>
│   └── *.json/lock
├── wheel <cache wheels used for seeding>
│   ├── house
│   │   └── *.whl <wheels downloaded go here>
│   └── <python major.minor> -> 3.9
│       ├── img-<version>
│       │   └── image
│       │           └── <install class> -> CopyPipInstall / SymlinkPipInstall
│       │               └── <wheel name> -> pip-20.1.1-py2.py3-none-any
│       └── embed
│           └── 1
│               └── *.json -> for every distribution contains data about newer embed versions and releases
└─── unzip <in zip app we cannot refer to some internal files, so first extract them>
     └── <virtualenv version>
         ├── py_info.py
         ├── debug.py
         └── _virtualenv.py
"""
from __future__ import absolute_import, unicode_literals

import json
import logging
from abc import ABCMeta
from contextlib import contextmanager
from hashlib import sha256

import six

from virtualenv.util.lock import ReentrantFileLock
from virtualenv.util.path import safe_delete
from virtualenv.util.six import ensure_text
from virtualenv.util.zipapp import extract
from virtualenv.version import __version__

from .base import AppData, ContentStore


class AppDataDiskFolder(AppData):
    """
    Store the application data on the disk within a folder layout.
    """

    def __init__(self, folder):
        self.lock = ReentrantFileLock(folder)

    def __repr__(self):
        return "{}".format(self.lock.path)

    @property
    def transient(self):
        return False

    def reset(self):
        logging.debug("reset app data folder %s", self.lock.path)
        safe_delete(self.lock.path)

    def close(self):
        """do nothing"""

    @contextmanager
    def locked(self, path):
        path_lock = self.lock / path
        with path_lock:
            yield path_lock.path

    @contextmanager
    def extract(self, path, to_folder):
        if to_folder is not None:
            root = ReentrantFileLock(to_folder())
        else:
            root = self.lock / "unzip" / __version__
        with root.lock_for_key(path.name):
            dest = root.path / path.name
            if not dest.exists():
                extract(path, dest)
            yield dest

    @property
    def py_info_at(self):
        return self.lock / "py_info" / "1"

    def py_info(self, path):
        return PyInfoStoreDisk(self.py_info_at, path)

    def py_info_clear(self):
        """"""
        py_info_folder = self.py_info_at
        with py_info_folder:
            for filename in py_info_folder.path.iterdir():
                if filename.suffix == ".json":
                    with py_info_folder.lock_for_key(filename.stem):
                        if filename.exists():
                            filename.unlink()

    def embed_update_log(self, distribution, for_py_version):
        return EmbedDistributionUpdateStoreDisk(self.lock / "wheel" / for_py_version / "embed" / "1", distribution)

    @property
    def house(self):
        path = self.lock.path / "wheel" / "house"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def wheel_image(self, for_py_version, name):
        return self.lock.path / "wheel" / for_py_version / "image" / "1" / name


@six.add_metaclass(ABCMeta)
class JSONStoreDisk(ContentStore):
    def __init__(self, in_folder, key, msg, msg_args):
        self.in_folder = in_folder
        self.key = key
        self.msg = msg
        self.msg_args = msg_args + (self.file,)

    @property
    def file(self):
        return self.in_folder.path / "{}.json".format(self.key)

    def exists(self):
        return self.file.exists()

    def read(self):
        data, bad_format = None, False
        try:
            data = json.loads(self.file.read_text())
            logging.debug("got {} from %s".format(self.msg), *self.msg_args)
            return data
        except ValueError:
            bad_format = True
        except Exception:  # noqa
            pass
        if bad_format:
            self.remove()
        return None

    def remove(self):
        self.file.unlink()
        logging.debug("removed {} at %s".format(self.msg), *self.msg_args)

    @contextmanager
    def locked(self):
        with self.in_folder.lock_for_key(self.key):
            yield

    def write(self, content):
        folder = self.file.parent
        try:
            folder.mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
        self.file.write_text(ensure_text(json.dumps(content, sort_keys=True, indent=2)))
        logging.debug("wrote {} at %s".format(self.msg), *self.msg_args)


class PyInfoStoreDisk(JSONStoreDisk):
    def __init__(self, in_folder, path):
        key = sha256(str(path).encode("utf-8") if six.PY3 else str(path)).hexdigest()
        super(PyInfoStoreDisk, self).__init__(in_folder, key, "python info of %s", (path,))


class EmbedDistributionUpdateStoreDisk(JSONStoreDisk):
    def __init__(self, in_folder, distribution):
        super(EmbedDistributionUpdateStoreDisk, self).__init__(
            in_folder, distribution, "embed update of distribution %s", (distribution,),
        )
