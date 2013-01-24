"""
----------------------------------------------------------------------
- urllib.request: urllib.request proxy
----------------------------------------------------------------------
- Copyright (C) 2011-2013  Orochimarufan
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
from __future__ import absolute_import, unicode_literals

from ..compat import PY3

if (PY3):
    from urllib.request import *
    from urllib.request import __file__, __doc__ #@UnresolvedImport @UnusedImport

else:
    import urllib as _urllib
    import urllib2 as _urllib2
    
    #########################################################################
    # urllib.request                                                        #
    #########################################################################
    URLError        = _urllib2.URLError
    HTTPError       = _urllib2.HTTPError
    request_host    = _urllib2.request_host
    Request         = _urllib2.Request
    urlopen         = _urllib2.urlopen
    install_opener  = _urllib2.install_opener
    OpenerDirector  = _urllib2.OpenerDirector
    build_opener    = _urllib2.build_opener
    
    BaseHandler             = _urllib2.BaseHandler
    AbstractHTTPHandler     = _urllib2.AbstractHTTPHandler
    AbstractBasicAuthHandler = _urllib2.AbstractBasicAuthHandler
    AbstractDigestAuthHandler = _urllib2.AbstractDigestAuthHandler
    HTTPHandler             = _urllib2.HTTPHandler
    HTTPErrorProcessor      = _urllib2.HTTPErrorProcessor
    HTTPDefaultErrorHandler = _urllib2.HTTPDefaultErrorHandler
    HTTPRedirectHandler     = _urllib2.HTTPRedirectHandler
    HTTPCookieProcessor     = _urllib2.HTTPCookieProcessor
    HTTPPasswordMgr         = _urllib2.HTTPPasswordMgr
    HTTPPasswordMgrWithDefaultRealm = _urllib2.HTTPPasswordMgrWithDefaultRealm
    HTTPBasicAuthHandler    = _urllib2.HTTPBasicAuthHandler
    HTTPDigestAuthHandler   = _urllib2.HTTPDigestAuthHandler
    ProxyHandler            = _urllib2.ProxyHandler
    ProxyBasicAuthHandler   = _urllib2.ProxyBasicAuthHandler
    ProxyDigestAuthHandler  = _urllib2.ProxyDigestAuthHandler
    FTPHandler              = _urllib2.FTPHandler
    CacheFTPHandler         = _urllib2.CacheFTPHandler
    FileHandler             = _urllib2.FileHandler
    UnknownHandler          = _urllib2.UnknownHandler
    if hasattr(_urllib2, "HTTPSHandler"):
        HTTPSHandler        = _urllib2.HTTPSHandler
    
    randombytes         = _urllib2.randombytes
    parse_keqv_list     = _urllib2.parse_keqv_list
    parse_http_list     = _urllib2.parse_http_list
    
    URLopener           = _urllib.URLopener
    FancyURLopener      = _urllib.FancyURLopener
    urlretrieve         = _urllib.urlretrieve
    
    __all__ = [i for i in globals().keys() if (i[0] != "_")]
