"""
----------------------------------------------------------------------
- compat.uni: String handling compatibility code
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
from __future__ import absolute_import, unicode_literals

from . import PY3

if PY3: # Python 3.x
    string_type = str
    byte_type = bytes
    text_type = str

    def b(s):
        if (isinstance(s, bytes)):
            return s
        return bytes(s, "UTF-8")
    
    def u(s):
        if (isinstance(s, str)):
            return s
        return str(s, "UTF-8")

    chr = chr
    unichr = chr
    unistr = str
    encstr = bytes

    def unicode_unescape(string):
        return bytes(string, "UTF-8").decode("unicode_escape")
    
    def unicode_escape(string):
        return str(string.encode("unicode_escape"), "UTF-8")
    
    string_unescape = unicode_unescape
    string_escape = unicode_escape

    def isstring(s):
        return isinstance(s, str)
    
    def isgenericstring(s):
        return isinstance(s, str) or isinstance(s, bytes)

    def nativestring(s):
        if (isinstance(s, str)):
            return s
        return str(s, "UTF-8")

else: # Python 2.x
    string_type = basestring
    byte_type = str
    text_type = unicode

    def b(s):
        return s
    
    def u(s):
        return unicode(s, "unicode_escape")

    chr = unichr
    unichr = unichr
    unistr = unicode
    encstr = bytes

    def unicode_unescape(string):
        return string.decode("unicode_escape")
    
    def unicode_escape(string):
        return string.encode("unicode_escape")
    
    def string_unescape(string):
        return string.decode("string_escape")
    
    def string_escape(string):
        return string.encode("string_escape")

    def isstring(s):
        return isinstance(s, str) or isinstance(s, unicode)
    isgenericstring = isstring

    def nativestring(s):
        if (isinstance(s, str)):
            return s
        return str(s)

b.__doc__ = """Bytes Literal"""
u.__doc__ = """Unicode Literal"""

__all__ = ["u", "b"]
