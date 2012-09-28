"""
@author Orochimarufan
@module libyo.compat.bltin
@created 2012-05-12
@modified 2012-05-12
"""

from __future__ import absolute_import, unicode_literals, division

from . import PY3
import sys

if PY3:
    import builtins
else:
    import __builtin__ as builtins

if sys.version_info >= (2,6):
    next = builtins.next
else:
    def next(iterator,default=None):
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
    __slots__=("metaclass",)
    def __init__(self,metaclass):
        self.metaclass=metaclass
    def __call__(self,klass):
        return self.metaclass(klass.__name__,klass.__bases__,dict(klass.__dict__))

if PY3:
    input = input
else:
    input = raw_input
