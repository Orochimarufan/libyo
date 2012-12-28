"""
----------------------------------------------------------------------
- utils.pretty: prettyfying utilities
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
from __future__ import absolute_import, unicode_literals, print_function


def fillP(string, length, filler=" "):
    string = str(string)
    return "".join([filler * (length - len(string)), string])


def fillA(string, length, filler=" "):
    string = str(string)
    return "".join([string, filler * (length - len(string))])


def prettyexc(header=None, notrace=False, ndash=60, **kargs):
    import traceback
    print("-" * ndash)
    if header:
        print(header)
    if notrace:
        import sys
        print("".join(traceback.format_exception_only(*sys.exc_info[:2], **kargs)), end="")
    else:
        traceback.print_exc(**kargs)
    print("-" * ndash)
