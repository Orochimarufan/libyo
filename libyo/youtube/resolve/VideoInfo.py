'''
Created on 01.02.2012

@author: hinata
'''

from __future__ import absolute_import, unicode_literals, division

from .. import exception
from ...util.Namespace import Namespace
from ...util.reflect import AliasVar

class VideoInfo(Namespace):
    """libYO.youtube.resolve.VideoInfo
    
    Holds Informations about a resolved video.
    
    functions:
        fmt_url(fmt): returns the URL for FMTCODE fmt.
        url(profile,quality): returns the URL for quality in profile
    
    items:
        video_id   : Video ID
        title      : Video Title
        uploader   : Video Uploader
        description: Video Description
        fmt_url_map: dict(FMT:URL)
        *          : More; depends on Backend
    """
    def __init__(self,flashvars):
        super(VideoInfo,self).__init__(flashvars);
    urlmap = AliasVar("fmt_url_map");
    def fmt_url(self,fmt):
        if int(fmt) not in self.fmt_url_map:
            raise exception.FMTNotAvailableError(self.video_id,fmt,self.fmt_url_map.keys(),self.title)
        return self.fmt_url_map[int(fmt)]
