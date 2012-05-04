"""
@author Orochimarufan
@module libyo.caching
@created 2011-11-28
@modified 2012-05-04
"""

from __future__ import absolute_import, unicode_literals, division

import datetime
import time

class CacheItem(object):
    value=None
    key=None
    expires=None
    def __init__(self,key,value,expires):
        self.value=value
        self.key=key
        if isinstance(expires,datetime.timedelta):
            self.durability=expires
            self.expires=datetime.datetime.now()+expires
        elif isinstance(expires, datetime.datetime):
            self.expires=expires
            self.durability=expires-datetime.datetime.now()
        else:
            raise ValueError("Expires has to be of type Datetime or Timedelta!")
    def expired(self,now=None):
        if now is None:
            now=datetime.datetime.now()
        return self.expires < now
    def get(self):
        return self.key,self.value
    def __repr__(self):
        return "".join(("<CacheItem '",self.key,"'=",self.val.__repr__()," expiring at '",self.expires.strftime("%c"),"'>"))
    def __getitem__(self,idx):
        if idx==3:
            return self.durability
        elif idx==2:
            return self.expires
        elif idx==1:
            return self.val
        elif idx==0:
            return self.key
        else:
            raise IndexError()
class CachePickleContainer(object):
    def __init__(self,li,dd,tp):
        self.main=li
        self.ddur=dd
        self.type=tp
    def create(self):
        return Cache(self,self.ddur,self.type)

class Cache(object):
    """libyo.caching.Cache
    Provides Cache Object with expiring Items"""
    default_duration=datetime.timedelta(hours=1)
    def __init__(self,other=None,default_duration=None,internal_type=dict):
        self._internal=internal_type()
        self._type=internal_type
        self._rlock=False
        self._last_refresh=time.time()
        if default_duration is not None:
            self.default_duration=default_duration
        if other is not None:
            self.extend(other)
    def extend(self,other):
        now=datetime.datetime.now()
        if other.__class__ is dict:
            self._list.extend(self._from_dict(other,now+self.default_duration))
        elif other.__class__ is self.__class__:
            self._list.extend(other._list)
        elif other.__class__ is CachePickleContainer:
            if self._type != other.type:
                raise ValueError("Types not matching. please use container.create()")
            self._list.extend(other.main)
            if self.default_duration!=other.ddur:
                self.default_duration=other.ddur
        else:
            raise ValueError("OTHER has to be of type DICT or CACHE")
        self._refresh()
    def _refresh(self):
        self.now=datetime.datetime.now()
        if self._rlock:
            return
        if (time.time()-self._last_refresh)<10:
            return
        self._rlock=True
        for k in [k for k,i in self._internal.items() if i.expired(self.now)]:
            del self._internal[k]
        self._rlock=False
        self._last_refresh=time.time()
    def __delitem__(self,key):
        self._refresh()
        del self._internal[key]
    def __setitem__(self,key,value,duration=None):
        self._refresh()
        if duration is None:
            duration=self.default_duration
        self._internal[key]=CacheItem(key,value,duration)
    def __getitem__(self,key):
        self._refresh()
        return self._internal[key].value
    def __contains__(self,key):
        self._refresh()
        return key in self._internal
    def __len__(self):
        return self._internal.__len__()
    def __dict__(self):
        return dict([i.get() for i in self._internal.values()])
    def __list__(self):
        return self._internal.values()
    def clear(self):
        self._internal=self._type()
    def items(self):
        self._refresh()
        return [x.get() for x in self._internal.values()]
    def keys(self):
        self._refresh()
        return self._internal.keys()
    def values(self):
        self._refresh()
        return [x.value for x in self._internal.values()]
    store=__setitem__
    retreive=__getitem__
    @staticmethod
    def _from_dict(other,expires):
        return dict([(k,CacheItem(k,v,expires)) for k,v in other.items()])
    def pickle_container(self):
        return CachePickleContainer(self)