'''
Created on 28.11.2011

@author: hinata
'''

from ..base import LibYoException

class YouTubeException(LibYoException):
    pass

class YouTubeResolveError(YouTubeException):
    def __init__(self,msg,video_id,video_title=None):
        self.video_id=video_id
        self.video_title=(video_title if video_title is not None else "")
        if msg is None:
            msg = "could not resolve video: "+video_id;
        super(YouTubeException,self).__init__(msg)

class FMTNotAvailableError(YouTubeResolveError):
    def __init__(self,video_id,fmt_requested,available_fmts=None,title=None):
        msg="FMT {0} not avaiable for Video with ID {1}".format(fmt_requested,video_id)
        if available_fmts is not None:
            msg="".join(msg,"\r\nAvaiable FMTs: ")
            msg="".join(msg,", ".join([str(x) for x in available_fmts]))
        super(YouTubeResolveError,self).__init__(msg,video_id,title)
        self.requested_fmt=fmt_requested
        self.available_fmt=(available_fmts if available_fmts is not None else [])

class BackendFailedException(YouTubeException):
    """This exception mustn't reach the end-user. it is used for flow-control!"""
    def __init__(self,exc=None):
        self.exc=exc
        super(YouTubeException,self).__init__()