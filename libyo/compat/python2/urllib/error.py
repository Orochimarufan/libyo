"""
@author Orochimarufan
@module libyo.compat.python2.urllib.error
@created 2012-05-04
@modified 2012-05-04
"""

from __future__ import absolute_import, unicode_literals, division
import urllib2 as _urllib2

#########################################################################
# urllib.error                                                          #
#########################################################################
URLError            = _urllib2.URLError;
HTTPError           = _urllib2.HTTPError;

__all__ = [ i for i in globals().keys() if i[0]!="_" ]