"""
----------------------------------------------------------------------
- youtube.resolve.core: core functions for resolving videos
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

from .WebBackend import WebBackend
from .EmbedBackend import EmbedBackend
from .MixBackend import MixBackend
from .CacheBackend import CacheBackend
from .YoutubeDLBackend import YoutubeDLBackend

from .Resolver import Resolver

backends = [
            WebBackend,
            EmbedBackend,
            CacheBackend,
            MixBackend,
            YoutubeDLBackend,
            ]


def set_default_resolver(resolver):
    global DEFAULT_RESOLVER
    DEFAULT_RESOLVER = resolver

if False: #cached
    DEFAULT_RESOLVER = Resolver(CacheBackend(MixBackend(
                                                        WebBackend(),
                                                        EmbedBackend(),
                                                        YoutubeDLBackend,
                                                        )
                                             ))
else: #uncached
    DEFAULT_RESOLVER = Resolver(MixBackend(
                                           WebBackend(),
                                           EmbedBackend(),
                                           YoutubeDLBackend(),
                                           ))


def resolve(vid, fmt):
    return DEFAULT_RESOLVER.resolve(vid).fmt_url(fmt)


def resolve2(vid, quality=None, mode="url"):
    """ZO YouTube Resolver V2 (Compatible)
    
    returnValue value = resolve2(YouTubeVideoID, YouTubeFMTCode=None, mode="url")
    
    ENUM mode:
    string "all":     return [ dict ] RV2 Result
    string "url":     return [string] YouTube Video URL
    string "map":     return [ dict ] RV2 Video Value ([COMPAT]=all)
    string "map6":    return [ list ] YouTube FMT-URL-MAP
    string "qa_list": return [ list ] RV2 Avaiable Qualities
    string "qa_map":  return [ dict ] RV2 Quality Map
    INFO: The YouTubeFMTCode Parameter is only used in "url" mode!
    
    You can look up the YouTubeFMTCode on Wikipedia:
        http://en.wikipedia.org/wiki/YouTube#Quality_and_codecs
    
    Resolve V2 Checks both the YouTube Video Site and the EmbeddedPlayer get_video_info API.
    For more information on either of them reffer to resolve2_getWeb() and resolve2_getEmbed()
    
    It will then parse the Player Parameters into multiple Dictionaries.
    The Parser is called resolve2_extract().
    
    Resolve V2 returns values based on the MODE Parameter."""
    if mode.lower() == "url" and quality is None:
        raise ValueError("Mode 'URL' Requires Parameter 'YouTubeQualityCode' to be set!")
    elif mode.lower() == "url":
        quality = int(quality)
    vid = str(vid)
    videoValue = DEFAULT_RESOLVER.resolve(vid)
    if mode.lower() == "all":
        return {"use": videoValue.map,
                "embed": None,
                "web": None}
    elif mode.lower() in ("map", "map2"):
        return videoValue.map
    elif mode.lower() == "url":
        return videoValue.fmt_url(quality)
    elif mode.lower() == "map6":
        return videoValue.map["fmt_stream_map"]
    elif mode.lower() == "qa_list":
        return videoValue.map["fmt_url_map"].keys()
    elif mode.lower() == "qa_map":
        return videoValue.map["fmt_url_map"]
    else:
        raise TypeError("""Parameter '{}' not in [ENUM mode].
        look up the possibilities in the docs!""")


def resolve3(video_id, resolver=None):
    """YO YouTube Video Resolver (V3)
    resolve3(video_id, resolver=None)
    
    Parameters:
        [ string ] video_id: The YouTube VideoID
        [Resolver] resolver: The libYO.youtube.resolve. Resolver instance to use. leave blank for default.
    
    returns a libyo.youtube.resolve.VideoInfo instance."""
    if resolver is None:
        resolver = DEFAULT_RESOLVER
    return resolver.resolve(video_id)
