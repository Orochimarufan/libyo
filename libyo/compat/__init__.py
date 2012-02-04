'''
Created on 28.11.2011

@author: hinata
'''
import sys
import importlib

if sys.version_info[0]<3:
    COMPAT="python2"
else:
    COMPAT="python3"

MODULE = importlib.import_module("libyo.compat."+COMPAT)

def getModule(name):
    return MODULE.getModule(name)