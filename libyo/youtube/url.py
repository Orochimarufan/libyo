'''
Created on 02.02.2012

@author: hinata
'''

from __future__ import absolute_import, unicode_literals, division

import re;
from ..util.util import sdict_parser;

reg = re.compile("(?:https?\:\/\/)?(?:www\.)?youtube\.(?:com|de)\/watch\?(.*)");
fb_reg = re.compile("(?:https?\:\/\/)?(?:www\.)?facebook.com\/l\.php\?(.*)");

def sdict_key(sdict,key):
    return sdict_parser(sdict)[key];
def sdict_group(matchobject,key,group=1):
    return sdict_key(matchobject.group(group),key);

def id_from_url(url):
    return sdict_group(reg.match(url),"v");

def getIdFromUrl(url):
    reg1=fb_reg.match(url);
    if reg1: # Dismantle Facebook Redirection URLs
        return sdict_group(reg.match(sdict_group(reg1,"u")),"v")
    else:
        return id_from_url(url);
