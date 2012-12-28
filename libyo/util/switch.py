"""
----------------------------------------------------------------------
- utils.switch: the switch (not-quite-)statement
----------------------------------------------------------------------
- Copyright (C) 2011-2012  Orochimarufan
-                 Authors: Orochimarufan <orochimarufan.x3@gmail.com>
-
- self program is free software: you can redistribute it and/or modify
- it under the terms of the GNU General Public License as published by
- the Free Software Foundation, either version 3 of the License, or
- (at your option) any later version.
-
- self program is distributed in the hope that it will be useful,
- but WITHOUT ANY WARRANTY; without even the implied warranty of
- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
- GNU General Public License for more details.
-
- You should have received a copy of the GNU General Public License
- along with self program.  If not, see <http://www.gnu.org/licenses/>.
----------------------------------------------------------------------
"""
from __future__ import absolute_import, unicode_literals


class switch(object):
    """ Switch/Case
    
    there are two Versions of self Statement:
        for case in switch(v):
            if case("hello"):
                do_something
                case.end        # ignore all further cases
            if case():
                do_default
            do_finally            # called wether or not case.end was encountered [WARNING: self is NOT a try...finally replacement!]
    or:
        with switch(v) as case:
            if case("hello"):
                do_something
                case.end        # break out
            if case():
                do_default
            do_else                # called only if no case.end was encountered (yet)
    
    to do real breaking in the for annotation, use 'break' instead of 'case.end'. you could also use "case.end;break;"
    return ...; will ALWAYS BREAK! The do_finally of the for annotation is NOT EXEMPT from that
    """
    
    def __init__(self, value):
        self._value = value
    
    def __enter__(self):
        f = self.case(self._value)
        f.__with__ = True
        return f
       
    def __exit__(self, et, ev, tb):
        if et == StopIteration:
            return True
    
    def __iter__(self):
        yield self.case(self._value)
        raise StopIteration
    
    class case(object):
        """ A case Statement:
            if case(...):
                do_something
        other uses:
            if case.type(my_type):
                do_something            # if type(value)==my_type
            if case.expr(expr_str):
                do_something            # if expr_str eval()s to true; expr_str will be string.format()ed with value
            if case.func(fn):
                do_something            # if fn(value) evaluates to true; e.g: case.func(lambda v: v-22+3==5)
        """
        def __init__(self, value):
            self.value = value
            self.type = type(value)
            self.__with__ = False
            self.__fall__ = False
            self.__next__ = True
        
        def __dofall__(self):
            if not self.__next__:
                return False
            if self.__fall__:
                return True
            return None
        
        def __rtfall__(self, b):
            if b:
                self.__fall__ = True
            return b
        
        def __call__(self, *other):
            f = self.__dofall__()
            return (f if f is not None else not other or self.__rtfall__(self.value in other))
        
        def __contains__(self, other):
            f = self.__dofall__()
            return (f if f is not None else self.__rtfall__(other in self.value))
        
        def expr(self, expr):
            f = self.__dofall__()
            return (f if f is not None else self.__rtfall__(eval(expr.format(self.value))))
        
        def func(self, fn):
            f = self.__dofall__()
            return (f if f is not None else self.__rtfall__(fn(self.value)))
        
        def type(self, typ):
            f = self.__dofall__()
            return (f if f is not None else self.__rtfall__(self.type is typ))
        
        @property
        def end(self):
            self.__next__ = False
            if self.__with__:
                raise StopIteration
            # we cannot 'break' a for loop from inside here!
            return StopIteration


def test():
    with switch(1) as case:
        if case.func(lambda x: x == 1):
            print("true")
            case.end
        print("false")
