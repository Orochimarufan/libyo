"""
----------------------------------------------------------------------
- youtube.auth: youtube api auth using oauth
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
how-to:
from libyo.youtube import auth

auth.init(my_client_secrets_file)
if not auth.login(my_login_file):
    url = auth.beginAuth(my_oauth_callback_url)
    <do something to get the code from the user>
    auth.finishAuth(code_from_user)

<for any requests that can be authenticated use>
auth.urlopen(my_url_or_request)

<to change accounts>
auth.logout()
"""
from __future__ import absolute_import, unicode_literals, division

from ..urllib import oauth2
from ..urllib import request
import json
import os

_cache = None
_secrets = None
_flow = None
_creds = None
_handler = None
_opener = None
_opener_raw = oauth2.urllibRequester.opener


def init(secrets_file):
    global _secrets
    with open(secrets_file) as fp:
        _secrets = json.load(fp)


def login(cache_file):
    global _creds, _cache
    _cache = cache_file
    if os.path.exists(_cache):
        with open(_cache, "rb") as fp:
            _creds = oauth2.Credentials.loadWithClientSecrets(fp, _secrets)
        _init2()
        return True
    else:
        return False


def _init2():
    global _handler, _opener
    _creds.update_cb = save
    _handler = oauth2.OAuthHandler(_creds)
    _opener = request.build_opener(_handler)


def urlopen(url):
    if _opener:
        return _opener.open(url)
    else:
        return _opener_raw.open(url)


def save():
    with open(_cache, "wb") as fp:
        _creds.dump(fp, False)


def beginAuth(callback_uri=oauth2.OOB_CALLBACK_URN):
    global _flow
    _flow = oauth2.Flow.fromClientSecrets(_secrets, "https://gdata.youtube.com/", callback_uri)
    return _flow.getAuthUrl()


def finishAuth(code):
    global _creds
    _creds = _flow.getTokens(code)
    save()
    _init2()


def logout():
    global _opener, _handler, _cache, _flow, _creds
    save()
    _opener = _handler = _cache = _flow = _creds = None
