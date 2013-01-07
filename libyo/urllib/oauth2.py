"""
----------------------------------------------------------------------
- urllib.oauth2: OAuth2 Facilities
----------------------------------------------------------------------
- Copyright (C) 2011-2013 Orochimarufan
-                Authors: Orochimarufan <orochimarufan.x3@gmail.com>
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
from __future__ import absolute_import, unicode_literals, division

from . import parse, request
from ..compat import uni
from ..base import LibyoError
import datetime
import json
import pickle
import logging
import io

OOB_CALLBACK_URN = 'urn:ietf:wg:oauth:2.0:oob'

GOOGLE_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'

logger = logging.getLogger(__name__)


# Exceptions
class OAuthError(LibyoError):
    pass


class OAuthTokenRefreshError(OAuthError):
    pass


class OAuthClientSecretsError(OAuthError):
    pass


class OAuthLoadError(OAuthError):
    pass


class UrllibRequester(object):
    def __init__(self, opener):
        self.opener = opener
    
    def __call__(self, url, method, data, headers):
        """ Unified Url-requesting function, Urllib implementation
        
        *url* the url as string
        *method* HTTP Method
        *data* POST Data
        *headers* HTTP Headers
        """
        if data is not None:
            data = uni.b(data)
        if method == 'POST' and data is None:
            data = b""
        r = request.Request(url, data, headers)
        fp = self.opener(r)
        content = fp.read()
        fp.close()
        return fp.getcode(), fp.headers, content

urllibRequester = UrllibRequester(request.build_opener())


class Credentials(object):
    """Stores the credentials"""
    def __init__(self, access_token, refresh_token, token_expiry,
                 client_id, client_secret, token_uri):
        """Create a new Credentials instance
        
        *access_token* is a string containing the Access Token
        
        *refresh_token* is a string containing the Refresh Token or
        ``None`` if none was provided
        
        *token_expiry* is a :class:`datetime.datetime` object that
        describes the Access Token expiry
        
        *client_id* is a string containing the Client ID
        
        *client_secret* is a string containing the Client Secret
        
        *token_uri* is a string containing a valid url pointing to
        the service's token page
        """
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expiry = token_expiry
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_uri = token_uri
        
        self.invalid = False
        self.stored = False
        
        self.update_cb = None
    
    def getAuthHeader(self):
        """Return the Authorization HTTP Header as tuple"""
        return 'Authorization', 'Bearer %s' % self.access_token
    
    def refresh(self, request_handler=urllibRequester):
        """Refresh the Access Token (only if a Refresh Token is available)
        
        *request_handler* a :function:`urllibRequester`-like callable
        that handles any HTTP requests done while refreshing
        """
        body = parse.urlencode({'grant_type': 'refresh_token',
                                'client_id': self.client_id,
                                'client_secret': self.client_secret,
                                'refresh_token': self.refresh_token})
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        
        code, headers, content = request_handler(self.token_uri, 'POST', body, headers)
        
        d = Flow._parse_token_response(content)
        if code == 200 and 'access_token' in d:
            self.access_token = d['access_token']
            self.refresh_token = d.get('refresh_token', self.refresh_token)
            if 'expires_in' in d:
                self.token_expiry = datetime.datetime.utcnow() +\
                                    datetime.timedelta(seconds=int(d['expires_in']))
                self.stored = False
                if self.update_cb:
                    self.update_cb()
        else:
            if 'error' in d:
                self.invalid = True
                raise OAuthTokenRefreshError(d['error'])
            raise OAuthTokenRefreshError('invalid response: %s.' % code)
    
    def isValid(self):
        """Return whether this Credentials can be used for authentification
        
        Returns:
            0 if we are invalid/cannot be refreshed
            1 if we need refreshing
            2 if we are good to go"""
        if self.invalid:
            return 0
        elif datetime.datetime.utcnow() > self.token_expiry:
            return 1
        else:
            return 2
    
    def __str__(self):
        valid = self.isValid()
        status = ""
        if valid == 0:
            status = "(invalid) "
        elif valid == 1:
            status = "(needs refreshing) "
        
        return "<Credentials access_token='%s' %sat %s>" % (self.access_token, status, hex(id(self)))
    
    #-----------------------------------------------------
    # Dump a credential to file
    def dump(self, fp, store_secret=True):
        data = {'client_id': self.client_id,
                'access_token': self.access_token,
                'refresh_token': self.refresh_token,
                'token_expiry': self.token_expiry,
                'token_uri': self.token_uri,
                'validity': self.isValid()}
        if store_secret:
            data['client_secret'] = self.client_secret
        pickle.dump(data, fp)
        self.stored = True
    
    def dumps(self, store_secret=True):
        with io.StringIO() as fp:
            self.dump(fp, store_secret)
            return fp.getvalue()
    
    #----------------------------------------------------
    # Load a dumped credential from file
    @classmethod
    def load(cls, fp, client_id=None, client_secret=None):
        data = pickle.load(fp)
        for prop_name in ('client_id', 'access_token', 'refresh_token',
                          'token_expiry', 'token_uri', 'validity'):
            if prop_name not in data:
                raise OAuthLoadError("Missing property: %s" % prop_name)
        if client_id is not None:
            if client_secret is None:
                raise OAuthLoadError("you need to specify both client_id and client_secret, or none")
            if data['client_id'] != client_id:
                raise OAuthLoadError("Client ID does not match: data='%s' app='%s'" % (data['client_id'], client_id))
            return cls(data['access_token'], data['refresh_token'], data['token_expiry'],
                       client_id, client_secret, data['token_uri'])
        if 'client_secret' not in data:
            raise OAuthLoadError("Stored Credentials are missing the Client Secret; you need to pass client_id and client_secret to load()")
        inst = cls(data['access_token'], data['refresh_token'], data['token_expiry'],
                   data['client_id'], data['client_secret'], data['token_uri'])
        
        if data['validity'] == 0:
            inst.invalid = True
        inst.stored = True
        
        return inst
    
    @classmethod
    def loads(cls, s, client_id=None, client_secret=None):
        with io.StringIO(s) as fp:
            return cls.load(fp, client_id, client_secret)
    
    @classmethod
    def loadWithClientSecrets(cls, fp, client_secrets):
        _, secrets = Flow._check_secrets(client_secrets)
        return cls.load(fp, secrets['client_id'], secrets['client_secret'])
    
    @classmethod
    def loadWithClientSecretsFile(cls, filename, cs_filename):
        with open(filename, "rb") as fp:
            with open(cs_filename) as cs:
                client_secrets = json.load(cs)
            return cls.loadWithClientSecrets(fp, client_secrets)


class Flow(object):
    """
    OAuth2 Authentication Flow
    """
    def __init__(self, client_id, client_secret, scope,
                  redirect_uri=OOB_CALLBACK_URN,
                  auth_uri=GOOGLE_AUTH_URI,
                  token_uri=GOOGLE_TOKEN_URI,
                  **kwargs):
        """
        *client_id* is a string containing the Client ID you get from
        the authorization provider when registering your application
        
        *client_secret* is a string containing the secret you get along
        with your Client ID
        
        *scope* is a string specifying the service you want to be authorized
        for
        
        *redirect_uri* is a string containing a redirection url that will
        receive the auth code
        
        *auth_uri* is a string containing a valid URL pointing to the
        authorization service provider's auth page
        
        *token_uri* is a string containing a valid URL pointing to the
        service provider's token exchange page
        
        *kwargs* can contain any other parameters you wish to pass to the
        authorization service
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.redirect_uri = redirect_uri
        self.auth_uri = auth_uri
        self.token_uri = token_uri
        self.params = {'access_type': 'offline',
                       'response_type': 'code'}
        self.params.update(kwargs)
    
    def getAuthUrl(self):
        """Return the URI the user has to authorize your app's access on"""
        query = {'client_id': self.client_id,
                 'redirect_uri': self.redirect_uri,
                 'scope': self.scope}
        query.update(self.params)
        parts = list(parse.urlparse(self.auth_uri))
        query.update(dict(parse.parse_qsl(parts[4])))
        parts[4] = parse.urlencode(query)
        return parse.urlunparse(parts)
    
    def getTokens(self, code, request_handler=urllibRequester):
        """Exchange the code for tokens
        
        *code* is a string containing the authorization code you get
        from redirecting the user to the URL returned by :meth:`getAuthUrl()`
        
        *request_handler* is a callable matching the signature of urllibRequester
        """
        code = uni.u(code)
        
        body = parse.urlencode({'grant_type': 'authorization_code',
                                'client_id': self.client_id,
                                'client_secret': self.client_secret,
                                'code': code,
                                'redirect_uri': self.redirect_uri,
                                'scope': self.scope})
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        
        status, headers, content = request_handler(self.token_uri,
                                                   'POST',
                                                   body,
                                                   headers)
        
        d = self._parse_token_response(content)
        if status == 200 and 'access_token' in d:
            access_token = d['access_token']
            refresh_token = d.get('refresh_token', None)
            token_expiry = None
            if 'expires_in' in d:
                token_expiry = datetime.datetime.utcnow() + \
                    datetime.timedelta(seconds=int(d['expires_in']))
            return Credentials(access_token, refresh_token, token_expiry,
                               self.client_id, self.client_secret,
                               self.token_uri)
    
    @staticmethod
    def _parse_token_response(content):
        content = uni.u(content)
        try:
            res = json.loads(content)
        except:
            res = dict(parse.parse_qsl(content))
        
        if res and 'expires' in res:
            res['expires_in'] = res.pop('expires')
        
        return res
    
    @staticmethod
    def _check_secrets(client_secrets):
        if client_secrets is None or len(client_secrets) != 1:
            raise OAuthClientSecretsError("not a Client Secrets dict: %s" % client_secrets)
        client_type, secrets = next(iter(client_secrets.items()))
        if client_type not in ('installed', 'web'):
            raise OAuthClientSecretsError("Unknown Client Type: %s" % client_type)
        required = ['client_id',
                    'client_secret',
                    'redirect_uris',
                    'auth_uri',
                    'token_uri']
        string = ['client_id',
                  'client_secret']
        for prop_name in required:
            if prop_name not in secrets:
                raise OAuthClientSecretsError(
                    "Missing property '%s'" % prop_name)
        for prop_name in string:
            if secrets[prop_name].startswith("[["):
                raise OAuthClientSecretsError(
                    "Property '%s' is not configured" % prop_name)
        
        #TODO: check redirect_uri against secrets['redirect_uris']
        
        return client_type, secrets
    
    @classmethod
    def fromClientSecrets(cls, client_secrets, scope, redirect_uri=OOB_CALLBACK_URN):
        """Create a Flow from a Client Secrets dict
        
        *client_secrets* is a dict as you get when JSON-parsing
        the client_secrets.json provided by some service providers
        
        *scope* is a string that contains the url-scope
        
        *redirect_uri* is a string containing a valid URL to redirect
        the code to
        """
        _, secrets = cls._check_secrets(client_secrets)
        
        return cls(secrets['client_id'], secrets['client_secret'], scope,
                   redirect_uri, secrets['auth_uri'], secrets['token_uri'])
    
    @classmethod
    def fromClientSecretsFile(cls, filename, scope, redirect_uri=OOB_CALLBACK_URN):
        """Create a Flow from a client_secrets.json file
        
        *filename* is a string containing the client_secrets.json filename
        
        *scope* is a string containing the uri-scope
        
        *redirect_uri* is a string containing the uri to redirect the code to
        """
        with open(filename) as fp:
            return cls.fromClientSecrets(json.load(fp), scope, redirect_uri)


class OAuthHandler(request.BaseHandler):
    """A urllib Handler to handle OAuth authentication using specific Credentials"""
    def __init__(self, creds):
        """Create new OAuthHandler
        
        *creds* is a valid :class:`Credentials` instance
        """
        self.creds = creds
    
    def http_request(self, req):
        #if self.creds.scope is not None:
        #    netloc1, path1 = parse.urlparse(req.get_full_url())[1:2]
        #    netloc2, path2 = parse.urlparse(self.creds.scope)[1:2]
        #    netloc1, netloc2 = netloc1.split(":")[0], netloc2.split(":")[0]
        #    path1 = path1[:len(path2)]
        #    if netloc1 == netloc2 and path1 == path2:
        #        return req
        
        req.add_header(*self.creds.getAuthHeader())
        return req
    
    def http_error_401(self, req, fp, code, msg, headers):
        logger.getChild("OAuthHandler").info("HTTP 401: auto-refreshing token")
        
        self.creds.refresh(UrllibRequester(self.parent))
        
        return self.parent.open(req)
