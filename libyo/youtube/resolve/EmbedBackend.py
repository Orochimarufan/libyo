'''
Created on 01.02.2012

@author: hinata
'''

from __future__ import absolute_import, unicode_literals, division

from .AbstractBackend import AbstractBackend
from .WebBackend import WebBackend
from ..exception import BackendFailedException
from ... import urllib
import logging

logger = logging.getLogger("libyo.youtube.resolve.EmbedBackend")


class EmbedBackend(AbstractBackend):
    base_url = "http://youtube.com/get_video_info?video_id="
    
    @staticmethod
    def _decode(data):
        try:
            return data.decode("UTF-8")
        except UnicodeDecodeError:
            return data.decode("Latin-1")
    
    def _resolve(self):
        logger.debug("resolve " + self.video_id)
        try:
            conn = urllib.request.urlopen(self.base_url + self.video_id)
        except (urllib.error.URLError, urllib.error.HTTPError):
            logger.warn("Connection Error", exc_info=True)
            return False
        else:
            data = conn.read()
            conn.close()
        f = WebBackend.fvars_parser(self._decode(data))
        if (not f):
            raise BackendFailedException("fvars parser returned false")
        if ("token" not in f or "reason" in f):
            raise BackendFailedException(f["reason"] if ("reason" in f) else "No Reason given.")
        return f
