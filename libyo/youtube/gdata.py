'''
Created on 29.11.2011

@author: hinata
'''

import json
from .. import compat
import re

urllib = compat.getModule("urllib");
html   = compat.getModule("html");
util   = compat.getModule("util");

def decode      ( byte ):
    """decodes BYTES with either UTF-8 OR Latin-1"""
    try:
        return byte.decode("UTF-8")
    except UnicodeDecodeError:
        return byte.decode("Latin-1")

def get_json    ( url ):
    """Retreives JSON URI and turns into Python Object"""
    return json.loads(decode(urllib.request.urlopen(url).read()))

def gdata   ( module, parameters = None, ssl = True ):
    """Retreive YouTube GData Module MODULE using parameters PARAMETERS.
    If SSL is true, HTTPS will be used to connect."""
    if parameters is None:
        parameters = list()
    parameters.append(("alt","jsonc")) #This Whole thing does not know xml... only JSON ;)
    
    base    = "{scheme}://gdata.youtube.com/feeds/api/{module}?{parameters}"
    scheme  = "https" if ssl else "http"
    params  = urllib.parse.urlencode(parameters)
    url     = base.format(scheme=scheme, module=module, parameters=params)
    
    request = urllib.request.Request(url)
    request.add_header  ("GData-Version", "2.0")
    
    return get_json (request)

def html_entity(entity):
    ent=entity[1:-1]
    if ent[0] == "#":
        # decoding by number
        if ent[1] != 'x':
            # number is in decimal
            return util.char(int(ent[1:]))
        else:
            # number is in hex
            return util.char(int('0x'+ent[2:], 16))
    else:
        # they were using a name
        if ent in html.entities: return html.entities[ent]
        else: return entity
def html_decode(text):
    def f(match):
        return html_entity(match.group(0))
    return re.sub("(\&.*\;)",f,text)
