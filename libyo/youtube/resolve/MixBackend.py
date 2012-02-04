'''
Created on 01.02.2012

@author: hinata
'''

from .AbstractBackend import AbstractBackend

class MixBackend(AbstractBackend):
    def __init__(self,*in_backends):
        self.backends=in_backends
        self.results=[]
    def _resolve(self):
        for backend in self.backends:
            backend.setup(self.video_id)
            result = backend.resolve()
            if result:
                return result
        return False

class __MixBackend2(MixBackend):
    def _resolve(self):
        self.results=[]
        for backend in self.backends:
            backend.setup(self.video_id)
            self.results.append(backend.resolve())
        mixed=dict()
        for result in self.results:
            if not result:
                continue
            for k,v in result.items():
                if k not in mixed:
                    mixed[k]=v
        return mixed