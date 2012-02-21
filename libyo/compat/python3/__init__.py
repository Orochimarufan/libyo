import importlib;

def getModule(name):
    if (name in ("configparser","html") ):#or name[:6]=="urllib"): #<- wont work.
        m=importlib.import_module(name);
        m.LIBYO_COMPAT="python3";
        m.LIBYO_TARGET="python3";
        return m;
    return importlib.import_module("."+name, "libyo.compat.python3");