"""
@author Orochimarufan
@module libyo.compat.python2.urllib.response
@created 2012-05-04
@modified 2012-05-04
"""

from __future__ import absolute_import, unicode_literals, division
import urllib as _urllib

#########################################################################
# urllib.response                                                       #
#########################################################################
# Python 2.x doen't implement the context protocol on addbase.          #
#########################################################################

addbase         = _urllib.addbase
def _addbase__enter__(self):
    if self.fp is None:
        raise ValueError("I/O Operation on closed file")
    return self
def _addbase__exit__(self, type, value, tb):
    self.close()
addbase.__enter__   = _addbase__enter__
addbase.__exit__    = _addbase__exit__

addclosehook    = _urllib.addclosehook
addinfo         = _urllib.addclosehook
addinfourl      = _urllib.addinfourl

__all__ = [ i for i in globals().keys() if i[0]!="_" ]
