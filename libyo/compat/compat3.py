#@PydevCodeAnalysisIgnore

from __future__ import print_function #to fix unittest
import sys
if sys.version_info[0]==3:
    
    import urllib.request
    import urllib.parse
    import html.entities
    
    htmlentities=html.entities.entitydefs
    urlopen=urllib.request.urlopen
    prn=print
    urlunquote=urllib.parse.unquote
    urlunquote_plus=urllib.parse.unquote_plus
    urlquote=urllib.parse.quote
    urllib_request=urllib.request.Request
    urlencode=urllib.parse.urlencode
    URLError=urllib.request.URLError
    HTTPError=urllib.request.HTTPError
    char=chr