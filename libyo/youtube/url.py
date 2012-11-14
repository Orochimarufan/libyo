'''
Created on 02.02.2012

@author: hinata
'''

from __future__ import absolute_import, unicode_literals, division

import re
from ..util.util import sdict_parser

regexp = re.compile(r"^(?:https?\:\/\/)?(?:www\.)?youtu(?:be\..{2,3}\/watch\?.*v\=.+(?:\&.+)*|\.be\/.+)$")
yt_reg = re.compile(r"^(?:https?\:\/\/)?(?:www\.)?youtube\..{2,3}\/watch\?(.*)$")
fb_reg = re.compile(r"^(?:https?\:\/\/)?(?:www\.)?facebook.com\/l\.php\?(.*)$")
be_reg = re.compile(r"^(?:https?\:\/\/)?(?:www\.)?youtu.be\/([^\/?]*)")

def sdict_key(sdict,key):
    return sdict_parser(sdict)[key]
def sdict_group(matchobject,key,group=1):
    return sdict_key(matchobject.group(group),key)

def unpack_redir(url):
    m = fb_reg.match(url)
    if m:
        return sdict_group(m, "u")
    return url

def id_from_url(url):
    m = yt_reg.match(url)
    if m:
        return sdict_group(m,"v")
    m = be_reg.match(url)
    if m:
        return m.group(1)
    raise ValueError("Not a valid Youtube.com/Youtu.be URL")

def getIdFromUrl(url):
    return id_from_url(unpack_redir(url))

