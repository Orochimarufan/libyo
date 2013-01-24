"""
----------------------------------------------------------------------
- compat.bltin: Builtins compatibility module
----------------------------------------------------------------------
- Copyright (C) 2011-2013  Orochimarufan
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
    import builtins #@UnresolvedImport @UnusedImport
else:
    import __builtin__ as builtins #@Reimport

if sys.version_info >= (2, 6):
    next = builtins.next #@ReservedAssignment
else:
    def next(iterator, default=None): #@ReservedAssignment
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
    input = input #@ReservedAssignment
else:
    input = raw_input #@ReservedAssignment

# exec_ acts like the python3 exec() function
try:
    exec_ = eval('exec')
except SyntaxError:
    def exec_(co, globals=None, locals=None): #@ReservedAssignment
        if globals is None:
            exec (co) #@UndefinedVariable
        elif locals is None:
            exec (co, globals) #@UndefinedVariable
        else:
            exec (co, globals, locals) #@UndefinedVariable
