'''
Created on 01.02.2012

@author: hinata
'''
from __future__ import absolute_import;
LIBYO_COMPAT="python2"
LIBYO_TARGET="python3"
import urllib as _urllib;
import urllib2 as _urllib2;
import urlparse as _urlparse;
import types as _types

#########################################################################
# urllib.parse                                                          #
#########################################################################
parse=_types.ModuleType("libyo.compat.python2.urllib.parse");
parse.quote           = _urllib.quote;
parse.quote_plus      = _urllib.quote_plus;
parse.unquote         = _urllib.unquote;
parse.unquote_plus    = _urllib.unquote_plus;
parse.unwrap          = _urllib.unwrap;
parse.urlencode       = _urllib.urlencode;

parse.splittype       = _urllib.splittype;
parse.splithost       = _urllib.splithost;
parse.splituser       = _urllib.splituser;
parse.splitpasswd     = _urllib.splitpasswd;
parse.splitport       = _urllib.splitport;
parse.splitnport      = _urllib.splitnport;
parse.splitquery      = _urllib.splitquery;
parse.splittag        = _urllib.splittag;
parse.splitvalue      = _urllib.splitvalue;
parse.splitattr       = _urllib.splitattr;

parse.clear_cache     = _urlparse.clear_cache;
parse.ParseResult     = _urlparse.ParseResult;
parse.SplitResult     = _urlparse.SplitResult;
parse.urlparse        = _urlparse.urlparse;
parse.urlunparse      = _urlparse.urlunparse;
parse.urlsplit        = _urlparse.urlsplit;
parse.urlunsplit      = _urlparse.urlunsplit;
parse.urljoin         = _urlparse.urljoin;
parse.urldefrag       = _urlparse.urldefrag;
parse.parse_qs        = _urlparse.parse_qs;
parse.parse_qsl       = _urlparse.parse_qsl;

#########################################################################
# urllib.request                                                        #
#########################################################################
request = _types.ModuleType("libyo.compat.python2.urllib.request");
request.URLError        = _urllib2.URLError;
request.HTTPError       = _urllib2.HTTPError;
request.request_host    = _urllib2.request_host;
request.Request         = _urllib2.Request;
request.urlopen         = _urllib2.urlopen;
request.install_opener  = _urllib2.install_opener;
request.OpenerDirector  = _urllib2.OpenerDirector;
request.build_opener    = _urllib2.build_opener;

request.BaseHandler             = _urllib2.BaseHandler;
request.AbstractHTTPHandler     = _urllib2.AbstractHTTPHandler;
request.AbstractBasicAuthHandler= _urllib2.AbstractBasicAuthHandler;
request.AbstractDigestAuthHandler=_urllib2.AbstractDigestAuthHandler;
request.HTTPHandler             = _urllib2.HTTPHandler;
request.HTTPErrorProcessor      = _urllib2.HTTPErrorProcessor;
request.HTTPDefaultErrorHandler = _urllib2.HTTPDefaultErrorHandler;
request.HTTPRedirectHandler     = _urllib2.HTTPRedirectHandler;
request.HTTPCookieProcessor     = _urllib2.HTTPCookieProcessor;
request.HTTPPasswordMgr         = _urllib2.HTTPPasswordMgr;
request.HTTPPasswordMgrWithDefaultRealm = _urllib2.HTTPPasswordMgrWithDefaultRealm;
request.HTTPBasicAuthHandler    = _urllib2.HTTPBasicAuthHandler;
request.HTTPDigestAuthHandler   = _urllib2.HTTPDigestAuthHandler;
request.ProxyHandler            = _urllib2.ProxyHandler;
request.ProxyBasicAuthHandler   = _urllib2.ProxyBasicAuthHandler;
request.ProxyDigestAuthHandler  = _urllib2.ProxyDigestAuthHandler;
request.FTPHandler              = _urllib2.FTPHandler;
request.CacheFTPHandler         = _urllib2.CacheFTPHandler;
request.FileHandler             = _urllib2.FileHandler;
request.UnknownHandler          = _urllib2.UnknownHandler;
if hasattr(_urllib2,"HTTPSHandler"):
    request.HTTPSHandler        = _urllib2.HTTPSHandler;

request.randombytes         = _urllib2.randombytes;
request.parse_keqv_list     = _urllib2.parse_keqv_list;
request.parse_http_list     = _urllib2.parse_http_list;

request.URLopener           = _urllib.URLopener;
request.FancyURLopener      = _urllib.FancyURLopener;
request.urlretrieve         = _urllib.urlretrieve;

#########################################################################
# urllib.error                                                          #
#########################################################################
error = _types.ModuleType("libyo.compat.python2.urllib.error");
error.URLError            = _urllib2.URLError;
error.HTTPError           = _urllib2.HTTPError;

#########################################################################
# urllib.response                                                       #
#########################################################################
response = _types.ModuleType("libyo.compat.python2.urllib.response");
response.addbase             = _urllib.addbase;
response.addclosehook        = _urllib.addclosehook;
response.addinfo             = _urllib.addinfo;
response.addinfourl          = _urllib.addinfourl;

import robotparser; #@UnusedImport