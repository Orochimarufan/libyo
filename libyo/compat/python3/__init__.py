import importlib;

def getModule(name):
    if (name[:4]=="html"):
        import html
        import html.entities
        import html.parser
    if (name in ("configparser","html","urllib") or name[:5]=="html." or name[:7]=="urllib."):
        m=importlib.import_module(name);
        return m;
    return importlib.import_module("."+name, "libyo.compat.python3");