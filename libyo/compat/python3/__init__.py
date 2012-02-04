import importlib;

def getModule(name):
    if (name=="configparser"):
        return importlib.import_module("configparser");
    if (name=="html"):
        return importlib.import_module("html");
    return importlib.import_module("."+name, "libyo.compat.python3");