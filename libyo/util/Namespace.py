"""
@author Orochimarufan
@module libyo.util.Namespace
@created 2012-02-18
@modified 2012-05-04
"""

from __future__ import absolute_import, unicode_literals, division

try:
    _sorted = sorted
except NameError:
    def _sorted(iterable, reverse=False):
        result = list(iterable)
        result.sort()
        if reverse:
            result.reverse()
        return result

class Namespace(dict):
    """A dict that is accessible by attribute notation."""
    def __init__(self,*args,**kwargs):
        super(Namespace,self).__init__(*args,**kwargs);
    def __getattribute__(self,key): 
        #For some weird reason we can't use __getattr__ here or it won't work with Data Descriptors.
        #AFAIK
        #def __getattr__(self,name):
        #    do_something
        #SHOULD equal
        #def __getattribute__(self,name):
        #    try:
        #        return super(class,self).__getattribute__(name)
        #    except AttributeError:
        #        do_something
        #Or am I wrong there?
        try:
            return super(Namespace,self).__getattribute__(key)
        except AttributeError:
            try:
                return self.__getitem__(key);
            except KeyError:
                raise AttributeError("<{0} object> has no Attribute '{1}'".format(self.__class__.__name__,key))
    def __setattr__(self,key,value):
        return self.__setitem__(key,value);
    def __delattr__(self,key):
        return self.__delitem__(key);
    def __setattribute__(self,key,value): #to set real attributes
        return super(Namespace,self).__setattr__(key,value);
    def __delattribute__(self,key): #to del real attributes
        return super(Namespace,self).__delattr__(key);
    def __repr__(self):
        name = self.__class__.__name__;
        items = list();
        for x,y in _sorted(self.items()):
            items.append("{0}={1}".format(repr(x),repr(y)));
        return "{0}({1})".format(name,", ".join(items));