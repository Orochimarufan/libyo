"""
----------------------------------------------------------------------
- youtube.Playlist: youtube Playlist handling
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

from .gdata import gdata, html_decode
import logging
from ..compat import htmlparser
from ..urllib import request

HAS_HTML = False # design changed


class Playlist(object):
    logger = logging.getLogger("libyo.youtube.Playlist")
    
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
    
    def _simple(self, params):
        return gdata("playlists/{0}".format(self.playlist_id), params)
    
    def simple(self, start=1, results=25):
        return self._simple([("start-index", start), ("max-results", results)])
    
    def skeleton(self):
        return self.simple(1, 1)
    
    def advanced(self):
        skel = self.skeleton()
        got = pos = 0
        pmax = skel["data"]["totalItems"]
        items = []
        while got < pmax:
            tmp = self.simple(got + 1, 50)
            if "items" not in tmp["data"]:
                self.logger.warn("Ran into a Wall while processing: PL[{}] MAX[{}] GOT[{}] POS[{}]; This needn't be bad, since YouTube may have 'flagged' some videos of your playlist.".format(self.playlist_id, pmax, got, pos))
                break
            for i in tmp["data"]["items"]:
                if i["position"] > pos:
                    pos = i["position"]
                items.append(i)
                got += 1
        skel["data"]["itemsPerPage"] = len(items)
        skel["data"]["items"] = items
        return skel
    if HAS_HTML:
        def noapi(self):
            page = request.urlopen("http://youtube.com/playlist?list="+self.playlist_id)
            layout = {"data":
                    {"description": "",
                     "title": None,
                     "items": [],
                     "itemsPerPage": 0,
                     "id": self.playlist_id,
                     "content": {"5": "http://www.youtube.com/p/" + self.playlist_id},
                     "startIndex": 1,
                     "author": None,
                     "totalItems": 0,
                     "thumbnail": {}
                     }, "apiVersion": "libyo-youtube-playlist-noapi/1.0"}
            document = htmlparser.parse(page).getroot()
            window = document.find_class("playlist-info")[0]
            layout["title"] = html_decode(window.find_class("playlist-reference")[0][0].text)
            layout["author"] = html_decode(window.find_class("channel-author-attribution")[0][0].text)
            window = document.find_class("playlist-landing")[0]
            items = window.find_class("playlist-video-item")
            for item in items:
                item_layout = {"position": int(item.find_class("video-index")[0].text),
                             "video": {
                                      "uploaded": "",
                                      "category": "",
                                      "updated": "",
                                      "rating": "",
                                      "description": "",
                                      "title": html_decode(item.find_class("video-title")[0].text),
                                      "tags": [],
                                      "thumbnail": {"hqDefault": item.find_class("video-thumb")[0][0][0].get("src")},
                                      "content": [],
                                      "player": [],
                                      "accessControl": {"comment": "allowed", "list": "allowed", "videoRespond": "moderated", "rate": "allowed", "syndicate": "allowed", "embed": "allowed", "commentVote": "allowed", "autoPlay": "allowed"},
                                      "uploader": None,
                                      "ratingCount": 0,
                                      "duration:": 0,
                                      "commentCount": 0,
                                      "likeCount": 0,
                                      "favoriteCount": 0,
                                      "id": None,
                                      "viewCount": 0},
                             "id": "",
                             "author": layout["author"]}
                try:
                    item_layout["video"]["id"] = item.find_class("yt-uix-button")[0].get("data-video-ids")
                except IndexError:
                    item_layout["video"]["id"] = ""
                try:
                    item_layout["video"]["uploader"] = html_decode(item.find_class("video-owner")[0][0].text)
                except IndexError:
                    item_layout["video"]["uploader"] = ""
                layout["data"]["items"].append(item_layout)
            return layout
        
        def mixed(self):
            api = self.advanced()
            
            def k(i):
                return int(i["position"])
            
            api["data"]["items"].sort(key=k)
            web = self.noapi()
            has = [i["position"] for i in api["data"]["items"]]
            has_id = [i["video"]["id"] for i in api["data"]["items"]]
            for i in web["data"]["items"]:
                if i["video"]["id"] not in has_id:
                    api["data"]["items"].append(i)
                    has.append(i["position"])
                    has_id.append(i["video"]["id"])
            api["data"]["items"].sort(key=k)
            for i in range(len(api["data"]["items"]) - 1):
                api["data"]["items"][i]["position"] = i + 1
            return api
    else:
        def noapi(self):
            self.logger.error("Playlist.noapi not avaiable")
        
        def mixed(self):
            self.logger.warn("noapi not avaiable. Playlist.mixed can only provide api data.")
            return self.advanced()
