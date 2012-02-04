'''
Created on 01.02.2012

@author: hinata
'''

char = unichr;
unistr = unicode;
encstr = bytes;

def unicode_unescape(string):
    return string.decode("unicode_escape");

def unicode_escape(string):
    return string.encode("unicode_escape");

def string_unescape(string):
    return string.decode("string_escape");

def string_escape(string):
    return string.encode("string_escape");

input=raw_input; #@ReservedAssignment