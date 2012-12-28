"""
----------------------------------------------------------------------
- utils.Namespace: dict-like object that gets accessed by attributes
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
    def __init__(self, *args, **kwargs):
        super(Namespace, self).__init__(*args, **kwargs)
        
    def __getattribute__(self, key):
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
            return super(Namespace, self).__getattribute__(key)
        except AttributeError:
            try:
                return self.__getitem__(key)
            except KeyError:
                raise AttributeError("<{0} object> has no Attribute '{1}'".format(self.__class__.__name__, key))
    
    def __setattr__(self, key, value):
        return self.__setitem__(key, value)
    
    def __delattr__(self, key):
        return self.__delitem__(key)
    
    def __setattribute__(self, key, value): #to set real attributes
        return super(Namespace, self).__setattr__(key, value)
    
    def __delattribute__(self, key): #to del real attributes
        return super(Namespace, self).__delattr__(key)
    
    def __repr__(self):
        name = self.__class__.__name__
        items = list()
        for x, y in _sorted(self.items()):
            items.append("{0}={1}".format(repr(x), repr(y)))
        return "{0}({1})".format(name, ", ".join(items))
