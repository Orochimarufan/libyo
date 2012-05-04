'''
Created on 01.02.2012

@author: hinata
'''

from __future__ import absolute_import, unicode_literals, division

from ...util.util import sdict_parser,unicode_unescape
from ..exception import BackendFailedException
import logging
logger  = logging.getLogger("libyo.youtube.resolve.WebBackend")
import libyo.compat
urllib  = libyo.compat.getModule("urllib");

try:
    import lxml.html
except ImportError:
    logger.warn("LXML not found. Please Install it from http://lxml.de for full functionality")
from .AbstractBackend import AbstractBackend

class WebBackend(AbstractBackend):
    FakeAgent="Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.121 Safari/535.2"
    base_url="http://www.youtube.com/watch?v="
    def _fetch_old(self):
        url="".join((self.base_url,str(self.video_id)))
        self.hook = urllib.request.urlopen(url)
    def _fetch(self):
        url="".join((self.base_url,str(self.video_id)))
        r=urllib.request.Request(url)
        r.add_header("UserAgent",self.FakeAgent)
        r.add_header("Referer","http://www.youtube.com")
        self.hook = urllib.request.urlopen(r)
    def _resolve(self):
        try:
            self._fetch()
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            logger.warn("Connection Error: "+str(e));
            return False
        if "lxml" in globals():
            return self._lxml()
        else:
            return self._re()
    @staticmethod
    def fvars_parser(fvars):
        main=sdict_parser(fvars,unq=0)
        if "url_encoded_fmt_stream_map" not in main:
            return False
        map6=[sdict_parser(i,unq=2) for i in urllib.parse.unquote(main["url_encoded_fmt_stream_map"]).split(",")]
        main=sdict_parser(fvars)
        main["fmt_stream_map"]=map6
        main["fmt_url_map"]=dict([(int(i["itag"]),i["url"]) for i in map6])
        return main
    #RE Part
    def _re(self):
        raise NotImplementedError()
    #LXML part
    def _lxml_data(self):
        try:
            div  = self.document.get_element_by_id("watch-video");
            scr  = div[2].text_content();
            ibgn = scr.index(" = \"")+4;
            iend = scr.index("\\n\";\n");
            strn = unicode_unescape(scr[ibgn:iend].strip());
            doc  = lxml.html.fragment_fromstring(strn);
            fvars= doc.get("flashvars")
        except KeyError:
            raise BackendFailedException()
        return self.fvars_parser(fvars)
    def _lxml_meta(self):
        ext={}
        ext["title"]= self.document.get_element_by_id("eow-title").get("title")
        ext["description"]= self.document.get_element_by_id("eow-description").text
        ext["uploader"]= self.document.find_class("author")[0].text
        return ext
    def _lxml(self):
        self.lxml = lxml.html.parse(self.hook)
        self.document = self.lxml.getroot()
        self.hook.close()
        data=self._lxml_data()
        data.update(self._lxml_meta())
        return data