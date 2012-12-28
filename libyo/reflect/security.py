"""
----------------------------------------------------------------------
- reflect.security: Python access-level security implementation (experimental)
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

import abc
from ..compat.reflect import func_code
from ..compat.bltin import withmetaclass
import inspect

#------------------------------------------------------------------------------
# Method Acccess Levels
#------------------------------------------------------------------------------
# Restrict Access from outside instance
#------------------------------------------------------------------------------


class SecurityException(Exception):
    pass


class CallError(Exception):
    pass

C_IM = 0
C_CM = 1
C_OU = 2
C_CA = 3


def CC_METHODS(self, context, owner):
    if context not in (C_IM, C_CM):
        raise CallError("@{0} must be used on Methods".format(type(self).__name__))


def CC_ANY(self, context, owner):
    pass


@withmetaclass(abc.ABCMeta)
class _FunctionAccess(object):
    def __init__(self, function):
        self.__func__ = function
        self.__code__ = func_code(function)
        self.__name__ = function.__name__
        self.__doc__ = function.__doc__
    
    def __get__(self, owner, otype=None):
        if (owner is None and type is not None):
            self.__context__(C_CM, otype)
            o = otype
        elif (owner is not None):
            self.__context__(C_IM, owner)
            o = owner
        else:
            raise Exception("Descriptor Error")
        self.__access__(inspect.currentframe().f_back, o)
        return self.__create__(owner, otype)
    
    def __call__(self, *args, **kwds):
        self.__context__(C_CA, None)
        self.__access__(inspect.currentframe().f_back, None)
        return self.__create__(None, None)(*args, **kwds)
    
    def __create__(self, owner, otype):
        if (owner is None and otype is None):
            return self.__func__
        return self.__func__.__get__(owner, otype)
    
    @abc.abstractmethod
    def __context__(self, context, owner):
        pass
    
    @abc.abstractmethod
    def __access__(self, frame, owner):
        pass


def _getframeself(frame):
    args = inspect.getargvalues(frame)
    #self is always first
    if len(args.args) < 1:
        return None
    name = args.args[0]
    return args.locals[name]


def _typeequals(a, b):
    if isinstance(a, type):
        return a == b
    else:
        return type(a) == b


def _issameinstance(a, b):
    if type(a) is super:
        return a.__self__ == b
    else:
        return a == b


def _null():
    pass


class private(_FunctionAccess):
    """ Restrict Access to current instance of class it was defined in """
    __context__ = CC_METHODS
    
    def __access__(self, frame, mself):
        fself = _getframeself(frame)
        if not _issameinstance(fself, mself) or self.__name__ not in type(fself).__dict__ \
          or type(fself).__dict__[self.__name__] != self:
            raise SecurityException("{0} was declared private.".format(self.__name__))


class protected(_FunctionAccess):
    """ Restrict Access to current instance """
    __context__ = CC_METHODS
    
    def __access__(self, frame, mself):
        fself = _getframeself(frame)
        if not _issameinstance(fself, mself):
            raise SecurityException("{0} was declared protected.".format(self.__name__))


class internal(_FunctionAccess):
    """ Restrict Access to current file """
    __context__ = CC_ANY
    
    def __access__(self, frame, mself):
        if frame.f_code.co_filename != self.__code__.co_filename:
            raise SecurityException("{0} was declared internal.".format(self.__name__))


def setaccessible(meth, mode):
    """ Disable Access Restrictions """
    if not isinstance(meth, _FunctionAccess):
        raise ValueError("Function Access not restricted: {0}".format(meth))
    if mode:
        if hasattr(meth, "__disaccess__"):
            raise ValueError("Access not unaccessible: {0}".format(meth))
        meth.__disaccess__ = meth.__access__
        meth.__access__ = _null
    else:
        if not hasattr(meth, "__disaccess__"):
            raise ValueError("Access not accessible: {0}".format(meth))
        meth.__access__ = meth.__disaccess__
        del meth.__disaccess__


def removerestrictions(meth):
    """ Return the raw method """
    if isinstance(meth, type(_null)):
        return meth
    elif not isinstance(meth, _FunctionAccess):
        raise ValueError("Function not access-restricted: {0}".format(meth))
    else:
        return removerestrictions(meth.__func__)

__all__ = ["SecurityException", "private", "protected", "internal"]

TESTS = """
# TESTs
@internal
def internal_test(text):
    print(text)

def internal_tester(text):
    internal_test(text)

class test_a(object):
    @private
    def private_test(self,text):
        print(text)
    @protected
    def protected_test(self,text):
        print(text)
    def private_tester(self,text):
        self.private_test(text)
    def protected_tester(self,text):
        self.protected_test(text)

class test_b(test_a):
    def private_tester(self,text):
        self.private_test(text)
    def protected_tester(self,text):
        self.protected_test(text)

class test_c(object):
    def private_tester(self,text):
        test_a.private_test(text)
    def protected_tester(self,text):
        test_a.protected_test(text)

def test_prio():
    test_a_ = test_a()
    try:
        test_a_.private_test("test_a.private_test: ok->fail")
    except SecurityException:
        print("test_a.private_test: fail->ok")
    test_a_.private_tester("test_a.private_tester: ok->ok")
    try:
        test_a_.protected_test("test_a.protected_test: ok->fail")
    except SecurityException:
        print("test_a.protected_test: fail->ok")
    test_a_.protected_tester("test_a.protected_tester: ok->ok")
    test_b_ = test_b()
    try:
        test_b_.private_tester("test_b.private_tester: ok->fail")
    except SecurityException:
        print("test_b.private_tester: fail->ok")
    test_b_.protected_tester("test_b.protected_tester: ok->ok")
    test_c_ = test_c()
    try:
        test_c_.private_tester("test_c.private_tester: ok->fail")
    except SecurityException:
        print("test_c.private_tester: fail->ok")
    try:
        test_c_.protected_tester("test_c.protected_tester: ok->fail")
    except SecurityException:
        print("test_c.protected_tester: fail->ok")
"""
