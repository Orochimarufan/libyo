'''
Created on 01.02.2012

@author: hinata
'''

from __future__ import absolute_import, unicode_literals, division

from ...caching import Cache
from .AbstractBackend import AbstractBackend
from datetime import timedelta

class CacheBackend(AbstractBackend):
    def __init__(self,backend):
        self.backend=backend
        self.cache=Cache(default_duration=timedelta(minutes=10))
    def clear(self):
        self.cache.clear()
    def _resolve(self):
        if self.video_id not in self.cache:
            self.backend.setup(self.video_id)
            result=self.backend.resolve()
            self.cache.store(self.video_id,result)
            return result
        else:
            return self.cache.retreive(self.video_id)
