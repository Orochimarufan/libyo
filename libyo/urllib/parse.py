"""
----------------------------------------------------------------------
- urllib.parse: urllib.parse proxy
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
    from urllib.parse import *
    from urllib.parse import __file__, __doc__ #@UnresolvedImport @UnusedImport

else:
    import urllib as _urllib
    import urlparse as _urlparse
    
    #########################################################################
    # urllib.parse                                                          #
    #########################################################################
    quote           = _urllib.quote
    quote_plus      = _urllib.quote_plus
    unquote         = _urllib.unquote
    unquote_plus    = _urllib.unquote_plus
    unwrap          = _urllib.unwrap
    urlencode       = _urllib.urlencode
    
    splittype       = _urllib.splittype
    splithost       = _urllib.splithost
    splituser       = _urllib.splituser
    splitpasswd     = _urllib.splitpasswd
    splitport       = _urllib.splitport
    splitnport      = _urllib.splitnport
    splitquery      = _urllib.splitquery
    splittag        = _urllib.splittag
    splitvalue      = _urllib.splitvalue
    splitattr       = _urllib.splitattr
    
    clear_cache     = _urlparse.clear_cache
    ParseResult     = _urlparse.ParseResult
    SplitResult     = _urlparse.SplitResult
    urlparse        = _urlparse.urlparse
    urlunparse      = _urlparse.urlunparse
    urlsplit        = _urlparse.urlsplit
    urlunsplit      = _urlparse.urlunsplit
    urljoin         = _urlparse.urljoin
    urldefrag       = _urlparse.urldefrag
    parse_qs        = _urlparse.parse_qs
    parse_qsl       = _urlparse.parse_qsl
    
    __all__ = [i for i in globals().keys() if (i[0] != "_")]
