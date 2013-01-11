"""
----------------------------------------------------------------------
- youtube.gdata: GData interface functions
----------------------------------------------------------------------
- Copyright (C) 2011-2012  Orochimarufan
-                 Authors: Orochimarufan <orochimarufan.x3@gmail.com>
-
- This program is free software: you can redistribute it and/or modify
- it under the terms of the GNU General Public License as published by
- the Free Software Foundation, either version 3 of the License, or
- (at your option) any later version.
-
- This program is distributed in the hope that it will be useful,
- but WITHOUT ANY WARRANTY; without even the implied warranty of
- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
- GNU General Public License for more details.
-
- You should have received a copy of the GNU General Public License
- along with this program.  If not, see <http://www.gnu.org/licenses/>.
----------------------------------------------------------------------
"""
from __future__ import absolute_import, unicode_literals, division

import json
import re

from ..compat import html, uni
from ..urllib import parse
from ..urllib import request
from ..util.util import sdict_parser

from . import auth


def decode(byte):
    """decodes BYTES with either UTF-8 OR Latin-1"""
    try:
        return byte.decode("UTF-8")
    except UnicodeDecodeError:
        return byte.decode("Latin-1")


#def get_json(url):
#    return json.load(urllib.request.urlopen(url))


def get_json(url):
    """Retreives JSON URI and turns into Python Object"""
    return json.loads(decode(auth.urlopen(url).read()))


def gdata(module, parameters=None, ssl=True):
    """Retreive YouTube GData Module MODULE using parameters PARAMETERS.
    If SSL is true, HTTPS will be used to connect."""
    if parameters is None:
        parameters = list()
    parameters.append(("alt", "jsonc")) #This Whole thing does not know xml... only JSON ;)
    
    base    = "{scheme}://gdata.youtube.com/feeds/api/{module}?{parameters}"
    scheme  = "https" if ssl else "http"
    if "?" in module:
        module, s = module.split("?", 1)
        d = sdict_parser(s)
        parameters.extend(d.items())
    params  = parse.urlencode(parameters)
    url     = base.format(scheme=scheme, module=module, parameters=params)
    #print(url)
    
    r = request.Request(url)
    r.add_header("GData-Version", "2.0")
    
    return get_json(r)


def html_entity(entity):
    ent = entity[1:-1]
    if ent[0] == "#":
        # decoding by number
        if ent[1] != 'x':
            # number is in decimal
            return uni.chr(int(ent[1:]))
        else:
            # number is in hex
            return uni.chr(int('0x' + ent[2:], 16))
    else:
        # they were using a name
        if ent in html.entities:
            return html.entities[ent]
        else:
            return entity


def html_decode(text):
    def f(match):
        return html_entity(match.group(0))
    return re.sub("(\&.*\;)", f, text)
