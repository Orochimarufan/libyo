'''
Created on 28.11.2011

@author: hinata
'''
import sys
import importlib

PY3 = sys.version_info[0]<3
COMPAT = "python3" if PY3 else "python2"

MODULE = importlib.import_module("libyo.compat."+COMPAT)

def getModule(name):
    return MODULE.getModule(name)