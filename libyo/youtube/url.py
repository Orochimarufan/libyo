'''
Created on 02.02.2012

@author: hinata
'''

import re;
from ..util.util import sdict_parser;

reg = re.compile("(?:https?\:\/\/)?(?:www\.)?youtube\.(?:com|de)\/watch\?(.*)");

def id_from_url(url):
    return sdict_parser(reg.match(url).group(1))["v"];