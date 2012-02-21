'''
Created on 19.02.2012

@author: hinata
'''

from ..compat import getModule as _compat
_urllib = _compat("urllib")
_request=_urllib.request
_parse=_urllib.parse
_error=_urllib.error
_response=_urllib.response
#_request = _compat("urllib.request")
#_parse = _compat("urllib.parse")
#_error = _compat("urllib.error")
#_response = _compat("urllib.response")
import posixpath as _posixpath
try: #GZip module may not be available
    import gzip as _gzip
except ImportError:
    HAS_GZIP=False
else:
    HAS_GZIP=True
import io as _io

#For completion purposes, import all handlers from the request module
BaseHandler             = _request.BaseHandler
AbstractHTTPHandler     = _request.AbstractHTTPHandler
AbstractBasicAuthHandler = _request.AbstractBasicAuthHandler
AbstractDigestAuthHandler = _request.AbstractDigestAuthHandler
HTTPHandler             = _request.HTTPHandler
HTTPErrorProcessor      = _request.HTTPErrorProcessor
HTTPDefaultErrorHandler = _request.HTTPDefaultErrorHandler
HTTPRedirectHandler     = _request.HTTPRedirectHandler
HTTPCookieProcessor     = _request.HTTPCookieProcessor
HTTPPasswordMgr         = _request.HTTPPasswordMgr
HTTPPasswordMgrWithDefaultRealm = _request.HTTPPasswordMgrWithDefaultRealm
HTTPBasicAuthHandler    = _request.HTTPBasicAuthHandler
HTTPDigestAuthHandler   = _request.HTTPDigestAuthHandler
ProxyHandler            = _request.ProxyHandler
ProxyBasicAuthHandler   = _request.ProxyBasicAuthHandler
ProxyDigestAuthHandler  = _request.ProxyDigestAuthHandler
FTPHandler              = _request.FTPHandler
CacheFTPHandler         = _request.CacheFTPHandler
FileHandler             = _request.FileHandler
UnknownHandler          = _request.UnknownHandler
if "HTTPSHandler" in _request.__dict__: #HTTPS support depends on the availability of the ssl module.
    HTTPSHandler        = _request.HTTPSHandler# therefore it cannot be guaranteed
#For reasons of ease we also adapt the build_opener function
build_opener            = _request.build_opener

class FancyHTTPRedirectHandler(HTTPRedirectHandler):
    """A Handler to add the capability to follow Relative Redirects in Urllib2"""
    @staticmethod
    def relative_redirect(old, new):
        if new.scheme !="": #An empty sheme indicates a relative redirect.
            return     new
        else:
            scheme     = old.scheme #use the same sheme as the request did
            netloc     = old.netloc #use the same netloc as the request did
            query      = new.query  #adapt the new query
            params     = new.params #adapt the new parameters
            fragment   = new.fragment #adapt the new fragments
            if new.path[0]=="/":    #semi-relative redirects just use the old sheme&netloc
                path   = new.path   #so adapt new path from site-root
            else:                   #real relative redirects specify a location relative to the current path
                path   = _posixpath.join(_posixpath.dirname(old.path), new.path)
            return _parse.ParseResult(scheme, netloc, path, params, query, fragment)
    def http_error_302(self, req, fp, code, msg, headers):
        # Some servers (incorrectly) return multiple Location headers
        # (so probably same goes for URI).  Use first header.
        if "location" in headers:
            newurl = headers["location"]
        elif "uri" in headers:
            newurl = headers["uri"]
        else:
            return
        
        # fix a possibly malformed URL
        urlparts = _parse.urlparse(newurl)
        
        # fill empty fields used to indicate relative redirects
        urlparts = self.relative_redirect(_parse.urlparse(req.full_url), urlparts)
        
        # For security reasons we don't allow redirection to anything other
        # than http, https or ftp.
        if not urlparts.scheme in ('http', 'https', 'ftp'):
            raise _error.HTTPError(newurl, code,
                            msg +
                            " - Redirection to url '%s' is not allowed" %
                            newurl,
                            headers, fp)
        
        if not urlparts.path:
            urlparts = list(urlparts)
            urlparts[2] = "/"
        newurl = _parse.urlunparse(urlparts)
        
        newurl = _parse.urljoin(req.full_url, newurl)
        
        # XXX Probably want to forget about the state of the current
        # request, although that might interact poorly with other
        # handlers that also use handler-specific request attributes
        new = self.redirect_request(req, fp, code, msg, headers, newurl)
        if new is None:
            return
        
        # loop detection
        # .redirect_dict has a key url if url was previously visited.
        if hasattr(req, 'redirect_dict'):
            visited = new.redirect_dict = req.redirect_dict
            if (visited.get(newurl, 0) >= self.max_repeats or
                len(visited) >= self.max_redirections):
                raise _error.HTTPError(req.full_url, code,
                                self.inf_msg + msg, headers, fp)
        else:
            visited = new.redirect_dict = req.redirect_dict = {}
        visited[newurl] = visited.get(newurl, 0) + 1
        
        # Don't close the fp until we are sure that we won't use it
        # with HTTPError.
        fp.read()
        fp.close()
        
        return self.parent.open(new, timeout=req.timeout)
    http_error_301 = http_error_303 = http_error_307 = http_error_302

if HAS_GZIP:
    class GZipEncodingHandler(BaseHandler):
        """A handler to add gzip capabilities to urllib2 requests
        """
        def http_request(self, req):                            #When sending a request,
            req.add_header("Accept-Encoding", "deflate, gzip")  #tell the server that we understand gzip
            return req
        def http_response(self, req, resp):                     #When we get our response
            if resp.headers.get("content-encoding") == "gzip":  #Check the content-encoding header
                gz = _gzip.GzipFile(                            #Create a GZipFile object
                            fileobj=_io.BytesIO(resp.read()),   #And open the stream
                            mode="r"
                          )
                old_resp = resp                                 #Save the original response
                resp = _response.addinfourl(gz,
                    old_resp.headers, old_resp.url, old_resp.code)#calculate new response
                resp.msg = old_resp.msg                         #Repopulate the attributes
                resp.modification = "gzip_decode"               #Let people know that we decoded this
                resp.modified = True                            #and that this isn't the original response
                resp.original = old_resp                        #append the original response
            return resp
        https_request = http_request                            #do the same for https requests
        https_response = http_response                          #do the same for https responses, too
