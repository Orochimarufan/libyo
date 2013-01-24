"""
----------------------------------------------------------------------
- urllib.response: urllib.response proxy
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
    from urllib.response import *
    from urllib.response import __file__, __doc__ #@UnresolvedImport @UnusedImport

else:
    import urllib as _urllib
    
    #########################################################################
    # urllib.response                                                       #
    #########################################################################
    # Python 2.x doen't implement the context protocol on addbase.          #
    #########################################################################
    
    def _addbase__enter__(self):
        if self.fp is None:
            raise ValueError("I/O Operation on closed file")
        return self
    
    def _addbase__exit__(self, etype, value, tb):
        self.close()
    
    addbase             = _urllib.addbase
    addbase.__enter__   = _addbase__enter__
    addbase.__exit__    = _addbase__exit__
    
    addclosehook    = _urllib.addclosehook
    addinfo         = _urllib.addclosehook
    addinfourl      = _urllib.addinfourl
    
    __all__ = [i for i in globals().keys() if (i[0] != "_")]
