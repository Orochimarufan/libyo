'''
Created on 28.11.2011

@author: hinata
'''
import sys
import importlib
import logging

from ..version import Version

PY3 = Version.PythonVersion.minVersion(3)
COMPAT = "python3" if PY3 else "python2"

logging.getLogger("libyo.compat").info("Running on {0}".format(Version.PythonVersion.formatString()))

MODULE = importlib.import_module("libyo.compat."+COMPAT)

def getModule(name):
    return MODULE.getModule(name)