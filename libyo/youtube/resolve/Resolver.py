'''
Created on 01.02.2012

@author: hinata
'''

from .VideoInfo import VideoInfo
from .. import exception

class Resolver(object):
    def __init__(self,backend):
        self.backend=backend
    def resolve(self,video_id):
        self.backend.setup(video_id)
        raw=self.backend.resolve()
        if not raw:
            raise exception.YouTubeResolveError(None,video_id)
        return VideoInfo(raw)