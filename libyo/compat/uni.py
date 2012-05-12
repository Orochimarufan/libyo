"""
@author Orochimarufan
@module libyo.compat.uni
@created 2012-05-04
@modified 2012-05-04
@inspired SIX
"""

from __future__ import absolute_import
from . import PY3

if PY3: # Python 3.x
    string_type = str
    byte_type = bytes
    text_type = str

    def b(s):
        return s.encode("UTF-8")
    def u(s):
        return s

    char = chr;
    unichr=chr;
    unistr=str;
    encstr=str;

    def unicode_unescape(string):
        return bytes(string,"utf-8").decode("unicode_escape");
    def unicode_escape(string):
        return str(string.encode("unicode_escape"),"utf-8");
    string_unescape=unicode_unescape;
    string_escape=unicode_escape;


else: # Python 2.x
    string_type = basestring
    byte_type = str
    text_type = unicode

    def b(s):
        return s
    def u(s):
        return unicode(s,"unicode_escape")

    char = unichr;
    unichr = unichr;
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

b.__doc__="""Bytes Literal"""
u.__doc__="""Unicode Literal"""

__all__ = ["u","b"]