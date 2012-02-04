#@PydevCodeAnalysisIgnore

from __future__ import print_function #needs to be first

import sys
if sys.version_info[0]==2:
    
    import urllib2
    import htmlentitydefs
    
    htmlentities=htmlentitydefs.entitydefs
    urlopen=urllib2.urlopen
    prn=print
    urlunquote=urllib2.unquote
    def urlunquote_plus(string):
        return urlunquote(string).replace("+"," ")
    urlquote=urllib2.quote
    urllib_request=urllib2.Request
    def urlencode(parameters):
        if parameters.__class__ is dict: parameters=parameters.items()
        return "&".join(["=".join([k,urllib2.quote(str(v))]) for k,v in parameters])
    char=unichr
    URLError = urllib2.URLError
    HTTPError = urllib2.HTTPError