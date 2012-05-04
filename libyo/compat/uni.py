"""
@author Orochimarufan
@module libyo.compat.uni
@created 2012-05-04
@modified 2012-05-04
@inspired SIX
"""

from __future__ import absolute_import
from . import PY3

if PY3:
    string_type = str
    byte_type = byte
    text_type = str

    def b(s):
        return s.encode("UTF-8")
    def u(s):
        return s
else:
    string_type = basestring
    byte_type = str
    text_type = unicode

    def b(s):
        return s
    def u(s):
        return unicode(s,"unicode_escape")

b.__doc__="""Bytes Literal"""
u.__doc__="""Unicode Literal"""

__all__ = ["u","b"]