"""
----------------------------------------------------------------------
- utils.reflect: reflection utilities
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

import weakref
import sys
from ..compat.bltin import withmetaclass

##############################################################################
# libyo.util.reflect
##############################################################################
# Reflect Utils using the Descriptor Protocol
# NOTE:
#  This classes are NOT supposed to be used in
#    multiple inheritance environments!
#  This classes use the super() call
##############################################################################


#------------------------------------------------------------------------------
# WeakMethod
#------------------------------------------------------------------------------
# Used to weakref Instance Methods
#------------------------------------------------------------------------------
class WeakMethod(object):
    def __init__(self, cb):
        try:
            try:
                self.inst = weakref.ref(cb.__self__)
            except TypeError:
                self.inst = None
            self.func = cb.__func__
            self.klass = cb.__self__.__class__
        except AttributeError:
            self.inst = None
            self.func = cb.__func__
            self.klass = None
    
    def __call__(self, *args, **kwargs):
        if self.inst is not None and self.inst() is None:
            raise ReferenceError
        elif self.inst is not None:
            mtd = self.func.__get__(self.inst())
        else:
            mtd = self.func
        return mtd(*args, **kwargs)


#------------------------------------------------------------------------------
# DescriptorObject
#------------------------------------------------------------------------------
# Base Object to allow Instance Descriptors
#------------------------------------------------------------------------------
class _DescriptorType(type):
    def __rawget__(self, name):
        return object.__getattribute__(self, name)
    
    def __rawset__(self, name, value):
        return type.__setattr__(self, name, value)
    
    def __setattr__(self, name, value):
        if hasattr(self, "__slots__"):
            if name not in self.__slots__:
                raise AttributeError("{0} has no Member {1}".format(self, name))
        v = object.__getattribute__(self, name)
        if hasattr(v, "__set__"):
            return v.__set__(self, value)
        return type.__setattr__(self, name, value)


@withmetaclass(_DescriptorType)
class DescriptorObject(object):
    def __rawget__(self, name):
        try: #self
            if hasattr(self, "__slots__"):
                if name not in self.__slots__:
                    raise AttributeError("{0} has no Member {1}".format(self, name))
            return self.__dict__[name]
        except KeyError: #bases
            e = sys.exc_info()[2]
            try:
                return type(self).__rawget__(type(self), name)
            except AttributeError:
                raise e
        
    def __rawset__(self, name, value):
        if hasattr(self, "__slots__"):
            if name not in self.__slots__:
                raise AttributeError("{0} has no Member {1}".format(self, name))
        self.__dict__[name] = value
    
    def __getattribute__(self, name):
        value = super(DescriptorObject, self).__getattribute__(name)
        if hasattr(value, '__get__'):
            value = value.__get__(self, self.__class__)
        return value
    
    def __setattr__(self, name, value):
        try:
            obj = super(DescriptorObject, self).__getattribute__(name)
        except AttributeError:
            pass
        else:
            if hasattr(obj, '__set__'):
                return obj.__set__(self, value)
        return super(DescriptorObject, self).__setattr__(name, value)


#------------------------------------------------------------------------------
# Various Data Descriptors
#------------------------------------------------------------------------------
# NOTE:
#    These Descriptors share the value per-descriptor (like class-vars)
#       you probably want to use it on a per-instance basis (inside constructor)
#------------------------------------------------------------------------------
class DataDescriptor(object):
    def __init__(self, value=None):
        super(DataDescriptor, self).__init__()
        self.value = value
    
    def __get__(self, obj, objtype=None):
        return self.value
    
    def __set__(self, obj, value):
        self.value = value
    
    def __delete__(self, obj):
        del self.value
        del self


class TypeVar(DataDescriptor):
    def __init__(self, type, value=None): #@ReservedAssignment
        if value is None:
            value = type()
        else:
            value = type(value)
        super(TypeVar, self).__init__(value)
        self.type = type
    
    def __set__(self, obj, value):
        self.value = self.type(value)


class TypeTriggerVar(TypeVar):
    def __init__(self, vtype, trigger, value=None): #@ReservedAssignment
        super(TypeTriggerVar, self).__init__(vtype, value)
        self.trigger = trigger
    
    def __set__(self, obj, value):
        self.value = self.type(value)
        self.trigger(self.value)
    
    def notrigger(self, value):
        self.value = self.type(value)


class TypeTriggerVar2(TypeTriggerVar):
    def __init__(self, type, trigger, value=None): #@ReservedAssignment
        super(TypeTriggerVar2, self).__init__(type, trigger, value)
        self.trigger(self.value)


#------------------------------------------------------------------------------
# new-style Data Descriptors
#------------------------------------------------------------------------------
# maps instances to values, only one instance on the
#------------------------------------------------------------------------------
class DataDescriptor2(DataDescriptor):
    def __init__(self, value=None):
        super(DataDescriptor2, self).__init__(value)
        self.values = weakref.WeakKeyDictionary()
    
    def __set__(self, obj, value):
        self.values[obj] = value
    
    def __get__(self, obj, objtype=None):
        if not obj:
            return self
        elif obj in self.values:
            return self.values[obj]
        else:
            return self.value


class SetterVar(DataDescriptor2):
    def __init__(self, f):
        super(SetterVar, self).__init__()
        self.setter = f
    
    def __set__(self, obj, value):
        super(SetterVar, self).__set__(self.setter(obj, value))


class TypeVar2(DataDescriptor2):
    def __init__(self, vtype, value=None):
        super(TypeVar2, self).__init__(value)
        self.type = vtype
    
    def __set__(self, obj, value):
        super(TypeVar2, self).__set__(obj, self.type(value))


class TypeTriggerVar3(TypeVar2):
    def __init__(self, vtype, trigger, value=None):
        super(TypeTriggerVar3, self).__init__(vtype, value)
        self.trigger = trigger
    
    def __set__(self, obj, value):
        super(TypeTriggerVar3, self).__set__(obj, value)
        self.trigger.__get__(obj)(super(TypeTriggerVar3, self).__get__(obj))
    
    def notrigger(self, obj, value):
        super(TypeTriggerVar3, self).__set__(obj, value)


#------------------------------------------------------------------------------
# Getter and Setter Function Factories
#------------------------------------------------------------------------------
# Use this in your Constructor to quickly add setters and getters
#------------------------------------------------------------------------------
def setterFunc(instance, varname):
    def setter(self, new):
        setattr(self, varname, new)
    return setter.__get__(instance)


def getterFunc(instance, varname):
    def getter(self):
        getattr(self, varname)
    return getter.__get__(instance)


def SetterDescriptor(object):
    def __init__(self, attr_name):
        self.attr_name = attr_name
   
    def __get__(self, obj, otype=None):
        if not obj:
            return self
        else:
            return lambda v: setattr(obj, self.attr_name, v)


def GetterDescriptor(object):
    def __init__(self, attr_name):
        self.attr_name = attr_name
    
    def __get__(self, obj, otype=None):
        if not obj:
            return self
        else:
            return lambda: getattr(obj, self.attr_name)


#------------------------------------------------------------------------------
# Alias Var
#------------------------------------------------------------------------------
# A data descriptor that redirects access to another attribute
#------------------------------------------------------------------------------
class AliasVar(object):
    __slots__ = ("name",)
    
    def __init__(self, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None and objtype is not None:
            return type.__getattribute__(objtype, self.name)
        return obj.__getattribute__(self.name)
    
    def __set__(self, obj, value):
        return obj.__setattr__(self.name, value)
