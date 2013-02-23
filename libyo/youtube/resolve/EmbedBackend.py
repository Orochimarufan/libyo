'''
Created on 01.02.2012

@author: hinata
'''

from __future__ import absolute_import, unicode_literals, division

from .AbstractBackend import AbstractBackend
from ..exception import BackendFailedException
from ... import urllib
from ...util.util import sdict_parser

import logging

logger = logging.getLogger(__name__)


class EmbedBackend(AbstractBackend):
    base_url = "http://youtube.com/get_video_info?video_id="
    
    @staticmethod
    def fvars_parser(fvars):
        main = sdict_parser(fvars, unq=0)
        if "url_encoded_fmt_stream_map" not in main:
            return False
        map6 = [sdict_parser(i, unq=2) for i in \
                urllib.parse.unquote(main["url_encoded_fmt_stream_map"]).split(",")]
        main = sdict_parser(fvars)
        main["fmt_stream_map"] = map6
        main["fmt_url_map"] = dict([
                                    (
                                     int(i["itag"]),
                                     "".join((i["url"], "&signature=", i["sig"]))
                                    ) for i in map6
                                   ])
        return main
    
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
        f = self.fvars_parser(self._decode(data))
        if (not f):
            raise BackendFailedException("fvars parser returned false")
        if ("token" not in f or "reason" in f):
            raise BackendFailedException(f["reason"] if ("reason" in f) else "No Reason given.")
        return f
