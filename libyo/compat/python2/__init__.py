import importlib

def getModule(name):
    return importlib.import_module("."+name, "libyo.compat.python2");