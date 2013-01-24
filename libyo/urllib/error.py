"""
----------------------------------------------------------------------
- urllib.error: urllib.error proxy
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
    from urllib.error import *
    from urllib.error import __file__, __doc__ #@UnresolvedImport @UnusedImport

else:
    import urllib2 as _urllib2

    #########################################################################
    # urllib.error                                                          #
    #########################################################################
    URLError            = _urllib2.URLError
    HTTPError           = _urllib2.HTTPError
    
    __all__ = [i for i in globals().keys() if (i[0] != "_")]
