"""
----------------------------------------------------------------------
- youtube.url: youtube url handling
----------------------------------------------------------------------
- Copyright (C) 2011-2012  Orochimarufan
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
from __future__ import absolute_import, unicode_literals, division

import re
from ..util.util import sdict_parser

regexp = re.compile(r"^(?:https?\:\/\/)?(?:www\.)?youtu(?:be\..{2,3}\/watch\?.*v\=.+(?:\&.+)*|\.be\/.+)$")
yt_reg = re.compile(r"^(?:https?\:\/\/)?(?:www\.)?youtube\..{2,3}\/watch\?(.*)$")
fb_reg = re.compile(r"^(?:https?\:\/\/)?(?:www\.)?facebook.com\/l\.php\?(.*)$")
be_reg = re.compile(r"^(?:https?\:\/\/)?(?:www\.)?youtu.be\/([^\/?]*)")


def sdict_key(sdict, key):
    return sdict_parser(sdict)[key]


def sdict_group(matchobject, key, group=1):
    return sdict_key(matchobject.group(group), key)


def unpack_redir(url):
    m = fb_reg.match(url)
    if m:
        return sdict_group(m, "u")
    return url


def id_from_url(url):
    m = yt_reg.match(url)
    if m:
        return sdict_group(m, "v")
    m = be_reg.match(url)
    if m:
        return m.group(1)
    raise ValueError("Not a valid Youtube.com/Youtu.be URL")


def getIdFromUrl(url):
    return id_from_url(unpack_redir(url))
