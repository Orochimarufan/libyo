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
addbase             = _urllib.addbase;
addclosehook        = _urllib.addclosehook;
addinfo             = _urllib.addinfo;
addinfourl          = _urllib.addinfourl;

__all__ = [ i for i in globals().keys() if i[0]!="_" ]