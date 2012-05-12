'''
libyo.type

Created on 29.11.2011

@author: hinata
'''

class PreservedOrderDict(object):
    '''
    classdocs
    '''
    def __init__(self,other=None):
        '''
        Constructor
        '''
        self._list=list()
        if other is not None:
            self.extend(other)
    def extend(self,other):
        '''
        Extend with:
            -dict
            -list of tuple
            -{0}
            -class.__dict__() object
        '''.format(self.__class__.__name__)
        if other.__class__ is dict:
            extensor=list(other.items())
        elif other.__class__ is list or other.__class__ is tuple:
            extensor=[(k,v) for (k,v) in other]
        elif other.__class__ is self.__class__:
            extensor=other._list
        elif hasattr(other,"__dict__"):
            extensor=list(other.__dict__().items())
        else:
            raise ValueError()
        self._list.extend(extensor)
    def keys(self):
        return (k for k,v in self._list)
    def items(self):
        return tuple(self._list)
    def values(self):
        return (v for k,v in self._list)
    def item(self,key):
        return key,self[key]
    def item_at(self,position):
        return self._list[position]
    def value_at(self,position):
        return self._list[position][1]
    def key_at(self,position):
        return self._list[position][0]
    def position_of(self,key):
        return self._list.index(self.item(key))
    def position_index(self,other):
        if other not in self.values():
            return -1
        return self.position_of(self.index(other))
    def index(self,other):
        if other not in self.values():
            return
        found=[k for k,v in self._list if v==other]
        return found[0]
    def __len__(self):
        return self._list.__len__()
    def __getitem__(self,key):
        return [v for k,v in self._list if k==key][0]
    def __setitem__(self,key,value):
        if key in self:
            del self[key]
        self._list.append((key,value))
    def __delitem__(self,key):
        self._list.remove(self.item(key))
    def __contains__(self,key):
        return key in self.keys()
    def dict(self):
        return dict(self._list)
    def list(self):
        return list(self._list)
    def tuple(self):
        return tuple(self._list)
