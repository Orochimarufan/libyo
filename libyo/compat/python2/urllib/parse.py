"""
@author Orochimarufan
@module libyo.compat.python2.urllib.parse
@created 2012-05-04
@modified 2012-05-04
"""

from __future__ import absolute_import, unicode_literals, division
import urllib as _urllib, urlparse as _urlparse

#########################################################################
# urllib.parse                                                          #
#########################################################################
quote           = _urllib.quote;
quote_plus      = _urllib.quote_plus;
unquote         = _urllib.unquote;
unquote_plus    = _urllib.unquote_plus;
unwrap          = _urllib.unwrap;
urlencode       = _urllib.urlencode;

splittype       = _urllib.splittype;
splithost       = _urllib.splithost;
splituser       = _urllib.splituser;
splitpasswd     = _urllib.splitpasswd;
splitport       = _urllib.splitport;
splitnport      = _urllib.splitnport;
splitquery      = _urllib.splitquery;
splittag        = _urllib.splittag;
splitvalue      = _urllib.splitvalue;
splitattr       = _urllib.splitattr;

clear_cache     = _urlparse.clear_cache;
ParseResult     = _urlparse.ParseResult;
SplitResult     = _urlparse.SplitResult;
urlparse        = _urlparse.urlparse;
urlunparse      = _urlparse.urlunparse;
urlsplit        = _urlparse.urlsplit;
urlunsplit      = _urlparse.urlunsplit;
urljoin         = _urlparse.urljoin;
urldefrag       = _urlparse.urldefrag;
parse_qs        = _urlparse.parse_qs;
parse_qsl       = _urlparse.parse_qsl;

__all__ = [ i for i in globals().keys() if i[0]!="_" ]
