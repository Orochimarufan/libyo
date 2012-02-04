'''
Created on 02.02.2012

@author: hinata
'''
import logging

def jimport(className,nameSpace=None):
    a=(className,className.split(".")[-1])
    b="from {0} import {1}".format(*a)
    c={}
    logging.getLogger("libyo.util.jimport").debug("'{0}'".format(className)+(" -> "+nameSpace.__name__ if nameSpace is not None else ""))
    exec (b,c) #@UndefinedVariable
    if nameSpace is not None:
        import types
        if isinstance(nameSpace,types.ModuleType):
            nameSpace.__dict__[a[1]]=c[a[1]]
        elif isinstance(nameSpace,type):
            setattr(nameSpace,a[1],c[a[1]])
        else:
            nameSpace[a[1]]=c[a[1]]
    return c[a[1]]