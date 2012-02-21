'''
Created on 02.02.2012

@author: hinata
'''

"DEPRECATED!!!!!!!!!!!!!!!!!"

def alias(func,*positional,**keyword):
    def __aliased(*args,**kwargs):
        args=positional+args
        kwargs=keyword+kwargs
        return func(*args,**kwargs)
    return __aliased

def typeVar2(instance,realvar,type,init=None): #@ReservedAssignment
    def getter(self):
        return self.__getattribute__(realvar)
    def setter(self,new):
        self.__setattr__(realvar,type(new))
    if init is None:
        init=type()
    instance.__setattr__(realvar,type(init))
    return property(getter.__get__(instance),setter.__get__(instance))

def typeTriggerVar(instance,realvar,type,trigger,init=None): #@ReservedAssignment
    def getter(self):
        return self.__getattribute__(realvar)
    def setter(self,new):
        self.__setattr__(realvar,type(new))
        trigger(self.__getattribute__(realvar))
    if init is None:
        init=type()
    instance.__setattr__(realvar,type(init))
    return property(getter.__get__(instance),setter.__get__(instance))
def typeTriggerVar2(instance,realvar,type,trigger,init=None): #@ReservedAssignment
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

def super1(arg1,arg2=None):
    """super1(obj) -> same as super(class,obj)
    super1(type) -> unbound super object
    super1(type,instance) -> bound super object
    super1(type,subtype) -> bound super object"""
    if arg2 is None:
        if isinstance(arg1,type):
            return super(arg1);
        elif isinstance(arg1,super):
            return super(arg1.__thisclass__,arg1);
        else:
            return super(arg1.__class__,arg1);
    else:
        return super(arg1,arg2);
def super2(arg1,arg2=None):
    """super2(obj) -> same as super(base,obj)
    super2(type) -> unbound super object
    super2(type,instance) -> bound super object
    super2(type,subtype) -> bound super object"""
    if arg2 is None:
        if isinstance(arg1,type):
            return super(arg1);
        elif isinstance(arg1,super):
            return super(arg1.__thisclass__.__base__,arg1);
        else:
            return super(arg1.__class__.__base__,arg1);
    else:
        return super(arg1,arg2);
#def _bound_super(self,arg1=None,arg2=None):
#        """super() -> same as super(base,self)
#        super(type) -> same as super(type,self)
#        super(None,type) -> unbound super object
#        super(type,instance) -> bound super object
#        super(type,subtype) -> bound super object"""
#        if arg2 is None:
#            if arg1 is None:
#                if isinstance(self,super):
#                    return super(self.__thisclass__.__base__,self);
#                return super(self.__class__.__base__,self);
#            else:
#                return super(arg1,self);
#        else:
#            if arg1 is None:
#                return super(arg2);
#            else:
#                return super(arg1,arg2);
#def superB(self):
#    """superB(self) -> py3k-like super function bound to object self
#    
#    super = superB(self)
#    super() -> same as super(base,self)
#    super(type) -> same as super(type,self)
#    super(None,type) -> unbound super object
#    super(type,instance) -> bound super object
#    super(type,subtype) -> bound super object
#    
#    Typical uses:
#        class A(MyBaseClass):
#            def __init__(self):
#                super=superB(self)
#                super().__init__()
#                #super() could be written in vanilla python 2.x:
#                #super(MyBaseClass,self)
#                #super(self.__class__.__base__,self)
#                ...
#        class B(MyBaseClass):
#            def __setattr__(self,name):
#                super=superB(self)
#                if condition:
#                    do_something
#                else:
#                    super(object).__setattr__(name,value)
#    
#    BEWARE:
#        superB(self)(type)        != super(type)
#        superB(self)(None,type)   == super(type)
#        superB(self)(type)        == super(type,self)
#    You should only use this wrapper to work with superB(self)() and superB(self)(type).
#    Use default super(type,object) for superB(self)(None,type) (see above) and superB(self)(type,instance|subtype)
#    """
#    return _bound_super.__get__(self);

class ReflectObject(object):
    """
    Inherit this to have transparent Properties
    """
    def __setattr__(self,name,value):
        try:
            return super(ReflectObject,self).__getattribute__(name).fset(value) #propset
        except AttributeError:
            pass
        super(ReflectObject,self).__setattr__(name,value) #realset
    def __getattribute__(self,name):
        try:
            return super(ReflectObject,self).__getattribute__(name).fget() #propget
        except AttributeError:
            pass
        return super(ReflectObject,self).__getattribute__(name) #real
