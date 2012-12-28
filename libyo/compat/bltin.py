"""
----------------------------------------------------------------------
- compat.bltin: Builtins compatibility module
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
import sys

if PY3:
    import builtins
else:
    import __builtin__ as builtins

if sys.version_info >= (2, 6):
    next = builtins.next
else:
    def next(iterator, default=None):
        try:
            return iterator.next()
        except StopIteration:
            if default is not None:
                return default
            else:
                raise


class withmetaclass(object):
    """ classdecorator for python 2 _and_ 3 metaclasses:
    python3:
        class a(object,metaclass=mymeta):
    python2:
        class a(object):
            __metaclass__ = mymeta
    withmetaclass:
        @withmetaclass(mymeta)
        class a(object):
    this works on both py2 and py3
    """
    __slots__ = ("metaclass",)
    
    def __init__(self, metaclass):
        self.metaclass = metaclass
    
    def __call__(self, klass):
        return self.metaclass(klass.__name__, klass.__bases__, dict(klass.__dict__))

if PY3:
    input = input
else:
    input = raw_input
