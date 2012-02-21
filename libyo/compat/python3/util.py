'''
Created on 01.02.2012

@author: hinata
'''

LIBYO_COMPAT="python3"
LIBYO_TARGET="libyo"

char = chr;
unistr=str;
encstr=str;

def unicode_unescape(string):
    return bytes(string,"utf-8").decode("unicode_escape");

def unicode_escape(string):
    return str(string.encode("unicode_escape"),"utf-8");

string_unescape=unicode_unescape;
string_escape=unicode_escape;

input=input; #@ReservedAssignment