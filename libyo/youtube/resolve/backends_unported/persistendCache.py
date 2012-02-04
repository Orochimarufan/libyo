'''
Created on 10.12.2011

@author: hinata
'''

from .cached import Cached as _parentBackend
from ....caching import Cache
from datetime import timedelta
import os, os.path
import pickle

class Cached(_parentBackend):
    def _resolve(self):
        if self.video_id not in self.cache:
            self.backend.setup(self.video_id)
            result=self.backend.resolve()
            self.cache.store(self.video_id,result)
            self._save()
            return result
        else:
            return self.cache.retreive(self.video_id)
    def __init__(self,backend):
        self.backend=backend
        self.binFile=os.path.expanduser("~/.config/libyo/youtube/rcache.bin")
        if not os.path.exists(self.binFile):
            if not os.path.isdir(os.path.dirname(self.binFile)):
                os.makedirs(os.path.dirname(self.binFile))
            self.cache=Cache(default_duration=timedelta(minutes=10))
            self._save()
        else:
            with open(self.binFile) as fp:
                self.cache=pickle.load(fp).create()
    def _save(self):
        with open(self.binFile) as fp:
            pickle.dump(self.cache.pickle_container(),fp)