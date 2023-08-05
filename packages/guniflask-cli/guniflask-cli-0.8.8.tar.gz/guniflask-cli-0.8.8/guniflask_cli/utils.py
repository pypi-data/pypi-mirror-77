# coding=utf-8

import sys
import tty
import termios
import os
from os.path import isfile, join, isdir
from importlib import import_module
from pkgutil import iter_modules
import re
import logging

from flask import Flask


def readchar():  # pragma: no cover
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def walk_modules(path: str):
    mods = []
    mod = import_module(path)
    mods.append(mod)
    if hasattr(mod, '__path__'):
        for _, subpath, ispkg in iter_modules(mod.__path__):
            fullpath = path + '.' + subpath
            if ispkg:
                mods += walk_modules(fullpath)
            else:
                submod = import_module(fullpath)
                mods.append(submod)
    return mods


def walk_files(path: str):
    files = []
    if isdir(path):
        names = os.listdir(path)
        for name in names:
            files += walk_files(join(path, name))
    elif isfile(path):
        files.append(path)
    return files


def pid_exists(pid):
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


_camelcase_invalid_chars = re.compile(r'[^a-zA-Z\d]')

_camelcase_split_chars = re.compile(r'(.)([A-Z][a-z]+)')
_camelcase_split_chars2 = re.compile(r'([a-z0-9])([A-Z])')


def string_camelcase(s):
    a = _camelcase_invalid_chars.split(s)
    return ''.join([(i[0].upper() + i[1:]) for i in a if i])


def string_lowercase_hyphen(s):
    return string_lowercase_underscore(s).replace('_', '-')


def string_lowercase_underscore(s):
    s = string_camelcase(s)
    s = _camelcase_split_chars.sub(r'\1_\2', s)
    return _camelcase_split_chars2.sub(r'\1_\2', s).lower()


def string_uppercase_underscore(s):
    return string_lowercase_underscore(s).upper()


def read_pid(pidfile):
    if isfile(pidfile):
        with open(pidfile, 'r') as f:
            line = f.readline()
            if line:
                pid = line.strip()
                if pid:
                    return int(pid)


def redirect_logger(name, logger):
    log = logging.getLogger(name)
    log.handlers = logger.handlers
    log.setLevel(logger.level)


def redirect_app_logger(app: Flask, logger):
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
