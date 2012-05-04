from ..compat import getModule as _
request=_("urllib.request") #TODO: redo this!
response=_("urllib.response")
error=_("urllib.error")
parse=_("urllib.parse")
robotparser=_("urllib.robotparser")

__all__ = ["download","handlers","request","response","error","parse","robotparser"]