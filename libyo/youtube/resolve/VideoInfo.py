'''
Created on 01.02.2012

@author: hinata
'''

from .. import exception

class VideoInfo(object):
    """libYO.youtube.resolve.VideoInfo
    
    Holds Informations about a resolved video.
    
    functions:
        fmt_url(fmt): returns the URL for FMTCODE fmt.
    
    items:
        title      : Video Title
        uploader   : Video Uploader
        description: Video Description
        fmt_stream_map: YouTube FMT/STREAM MAP
        fmt_url_map: dict(FMT:URL)
        *          : More
    """
    def __init__(self,infomap,urlmap):
        self.map=infomap
        self.urlmap=urlmap
    def fmt_url(self,fmt):
        if int(fmt) not in self.urlmap:
            raise exception.FMTNotAvailableError(self.video_id,fmt,self._urlmap.keys(),self.title)
        return self.urlmap[int(fmt)]
    def __getattr__(self,name):
        try:
            return super(object).__getattr__(name)
        except AttributeError:
            try:
                return self.map[name]
            except IndexError:
                raise AttributeError()
    def __getitem__(self,key):
        return self.map[key]
