"""
----------------------------------------------------------------------
- type: some types
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


class PreservedOrderDict(object):
    '''
    classdocs
    '''
    def __init__(self, other=None):
        '''
        Constructor
        '''
        self._list = list()
        if other is not None:
            self.extend(other)
    
    def extend(self, other):
        '''
        Extend with:
            -dict
            -list of tuple
            -{0}
            -class.__dict__() object
        '''.format(self.__class__.__name__)
        if other.__class__ is dict:
            extensor = list(other.items())
        elif other.__class__ is list or other.__class__ is tuple:
            extensor = [(k, v) for (k, v) in other]
        elif other.__class__ is self.__class__:
            extensor = other._list
        elif hasattr(other, "__dict__"):
            extensor = list(other.__dict__().items())
        else:
            raise ValueError()
        self._list.extend(extensor)
    
    def keys(self):
        return (k for k, v in self._list)
    
    def items(self):
        return tuple(self._list)
    
    def values(self):
        return (v for k, v in self._list)
    
    def item(self, key):
        return key, self[key]
    
    def item_at(self, position):
        return self._list[position]
    
    def value_at(self, position):
        return self._list[position][1]
    
    def key_at(self, position):
        return self._list[position][0]
    
    def position_of(self, key):
        return self._list.index(self.item(key))
    
    def position_index(self, other):
        if other not in self.values():
            return -1
        return self.position_of(self.index(other))
    
    def index(self, other):
        if other not in self.values():
            return
        found = [k for k, v in self._list if v == other]
        return found[0]
    
    def __len__(self):
        return self._list.__len__()
    
    def __getitem__(self, key):
        return [v for k, v in self._list if k == key][0]
    
    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        self._list.append((key, value))
    
    def __delitem__(self, key):
        self._list.remove(self.item(key))
    
    def __contains__(self, key):
        return key in self.keys()
    
    def dict(self):
        return dict(self._list)
    
    def list(self):
        return list(self._list)
    
    def tuple(self):
        return tuple(self._list)
