'''
Created on 21.02.2012

@author: hinata
'''

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

import weakref
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

class DescriptorObject(object):
    def __getdescriptor__(self,name): #THIS ONLY WORKS ON INSTANCE DESCRIPTORS!
        value = super(DescriptorObject,self).__getattribute__(name);
        if not hasattr(value,'__get__'):
            raise AttributeError("%s is no valid Descriptor!"%name);
        return value;
    def __getattribute__(self,name):
        value = super(DescriptorObject,self).__getattribute__(name);
        if hasattr(value,'__get__'):
            value = value.__get__(self,self.__class__);
        return value
    def __setattr__(self,name,value):
        try:
            obj = super(DescriptorObject,self).__getattribute__(name);
        except AttributeError:
            pass
        else:
            if hasattr(obj,'__set__'):
                return obj.__set__(self,value);
        return super(DescriptorObject,self).__setattr__(name,value);

#------------------------------------------------------------------------------
# Various Data Descriptors
#------------------------------------------------------------------------------
# NOTE:
#    To use InstanceMethods in TypeTriggerVar*s, you need to inherit
#        DescriptorObject and move the Descriptor definitions into the
#        Constructor.
#------------------------------------------------------------------------------

class DataDescriptor(object):
    def __init__(self,value=None):
        super(DataDescriptor,self).__init__();
        self.value=value;
    def __get__(self,obj,objtype=None):
        return self.value;
    def __set__(self,obj,value):
        self.value=value;
    def __delete__(self,obj):
        del self.value;
        del self;

class TypeVar(DataDescriptor):
    def __init__(self,type,value=None): #@ReservedAssignment
        if value is None:
            value = type();
        else:
            value = type(value);
        super(TypeVar,self).__init__(value);
        self.type=type;
    def __set__(self,obj,value):
        self.value=self.type(value);

class TypeTriggerVar(TypeVar):
    def __init__(self,vtype,trigger,value=None): #@ReservedAssignment
        super(TypeTriggerVar,self).__init__(vtype,value);
        self.trigger    = trigger;
    def __set__(self,obj,value):
        self.value=self.type(value);
        self.trigger(self.value);
    def notrigger(self,value):
        self.value=self.type(value);

class TypeTriggerVar2(TypeTriggerVar):
    def __init__(self,type,trigger,value=None): #@ReservedAssignment
        super(TypeTriggerVar2,self).__init__(type,trigger,value);
        self.trigger(self.value);

class AliasVar(DataDescriptor):
    def __init__(self,name):
        self.name=name
    def __get__(self,obj,objtype=None):
        if obj is None and objtype is not None:
            return type.__getattribute__(objtype,self.name)
        return obj.__getattribute__(self.name)
    def __set__(self,obj,value):
        return obj.__setattr__(self.name,value)

#------------------------------------------------------------------------------
# Getter and Setter Function Factories
#------------------------------------------------------------------------------
# Use this in your Constructor to quickly add setters and getters
#------------------------------------------------------------------------------

def setterFunc(instance,varname):
    def setter(self,new):
        self.__setattr__(varname,new)
    return setter.__get__(instance)

def getterFunc(instance,varname):
    def getter(self):
        self.__getattr__(varname)
    return getter.__get__(instance)
