'''
Created on 18.02.2012

@author: hinata
'''

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
    def __getattr__(self,key):
        return self.__getitem__(key);
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