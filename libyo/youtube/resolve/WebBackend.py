"""
----------------------------------------------------------------------
- youtube.resolve.WebBackend: parse the watch page and extract info
----------------------------------------------------------------------
- Copyright (C) 2011-2012  Orochimarufan
-                 Authors: Orochimarufan <orochimarufan.x3@gmail.com>
-
- This program is free software: you can redistribute it and/or modify
- it under the terms of the GNU General Public License as published by
- the Free Software Foundation, either version 3 of the License, or
- (at your option) any later version.
-
- This program is distributed in the hope that it will be useful,
- but WITHOUT ANY WARRANTY; without even the implied warranty of
- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
- GNU General Public License for more details.
-
- You should have received a copy of the GNU General Public License
- along with this program.  If not, see <http://www.gnu.org/licenses/>.
----------------------------------------------------------------------
"""
from __future__ import absolute_import, unicode_literals, division

import json
import logging
logger  = logging.getLogger("libyo.youtube.resolve.WebBackend")

from ...compat.uni import unicode_unescape
from ...util.util import sdict_parser
from ..exception import BackendFailedException
from ... import urllib
from ...compat import htmlparser

if htmlparser.IMPL != "lxml": #@UndefinedVariable
    logger.warn("LXML not avaiable. Please Install it from http://lxml.de for full functionality and performance!")

from .AbstractBackend import AbstractBackend


class WebBackend(AbstractBackend):
    FakeAgent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4"
    base_url = "http://www.youtube.com/watch?v="
    
    def open_page(self):
        url = "".join((self.base_url, str(self.video_id)))
        r = urllib.request.Request(url)
        r.add_header("UserAgent", self.FakeAgent)
        r.add_header("Referer", "http://www.youtube.com")
        self.hook = urllib.request.urlopen(r)

    def unpack_data(self):
        #2013-02-14: youtube now uses JS completely
        div = self.document.get_element_by_id("watch7-video")
        src = div[1].text
        ibgn = src.index(" = {") + 3
        iend = src.rindex("};") + 1
        strn = unicode_unescape(src[ibgn:iend].strip())
        # hope that it'll be valud JSON
        fvars = json.loads(strn)["args"]
        fvars["fmt_stream_map"] = [sdict_parser(i, unq=2) for i in fvars["url_encoded_fmt_stream_map"].split(",")]
        fvars["fmt_url_map"] = dict([(
                                      int(i["itag"]),
                                      "&signature=".join((i["url"], i["sig"]))
                                     ) for i in fvars["fmt_stream_map"]])
        return fvars
    
    def unpack_meta(self):
        ext = {}
        # "title" is now in the fvars data
        #ext["title"] = self.document.get_element_by_id("watch-headline-title")[0].get("title")
        #ext["title"] = [i for i in self.document.get_element_by_id("watch7-container") if i.tag == "meta" and i.get("itemprop") == "name"][0].get("content")
        ext["description"] = self.document.get_element_by_id("eow-description").text
        ext["uploader"] = self.document.get_element_by_id("watch7-user-header")[1].text
        return ext
    
    def _resolve(self):
        try:
            self.open_page()
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            raise BackendFailedException(e)
        self.lxml = htmlparser.parse(self.hook)
        self.document = self.lxml.getroot()
        self.hook.close()
        data = self.unpack_data()
        data.update(self.unpack_meta())
        return data

