'''
Created on 02.02.2012

@author: hinata
'''

def alias(func,*positional,**keyword):
    def __aliased(*args,**kwargs):
        args=positional+args
        kwargs=keyword+kwargs
        return func(*args,**kwargs)
    return __aliased

def typeVar2(instance,realvar,type,init=None):
    def getter(self):
        return self.__getattribute__(realvar)
    def setter(self,new):
        self.__setattr__(realvar,type(new))
    if init is None:
        init=type()
    instance.__setattr__(realvar,type(init))
    return property(getter.__get__(instance),setter.__get__(instance))

def typeTriggerVar(instance,realvar,type,trigger,init=None):
    def getter(self):
        return self.__getattribute__(realvar)
    def setter(self,new):
        self.__setattr__(realvar,type(new))
        trigger(self.__getattribute__(realvar))
    if init is None:
        init=type()
    instance.__setattr__(realvar,type(init))
    return property(getter.__get__(instance),setter.__get__(instance))
def typeTriggerVar2(instance,realvar,type,trigger,init=None):
    def getter(self):
        return self.__getattribute__(realvar)
    def setter(self,new):
        self.__setattr__(realvar,type(new))
        trigger(self.__getattribute__(realvar))
    if init is None:
        init=type()
    instance.__setattr__(realvar,type(init))
    trigger(instance.__getattribute__(realvar))
    return property(getter.__get__(instance),setter.__get__(instance))

def setterFunc(instance,varname):
    def setter(self,new):
        self.__setattr__(varname,new)
    return setter.__get__(instance)

def super2(self):
    return super(self.__class__,self)

class ReflectObject(object):
    """
    Inherit this to have transparent Properties
    """
    def __setattr__(self,name,value):
        try:
            super(object,self).__getattribute__(name).fset(value)
        except AttributeError:
            super(object,self).__setattr__(name,value)
    def __getattribute__(self,name):
        try:
            return super(object,self).__getattribute__(name).fget()
        except AttributeError:
            return super(object,self).__getattribute__(name)
