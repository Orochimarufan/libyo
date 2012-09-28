'''
Created on 28.11.2011

@author: hinata
'''
import sys
import importlib
import logging
import platform

PY3 = sys.version_info >= (3,)
COMPAT = "python3" if PY3 else "python2"

logging.getLogger("libyo.compat").info("Running on {0} {1} {2}".format(platform.python_implementation(), ".".join(map(str,sys.version_info[:3])), sys.version_info[3]))

MODULE = importlib.import_module("libyo.compat."+COMPAT)

def getModule(name):
    return MODULE.getModule(name)
