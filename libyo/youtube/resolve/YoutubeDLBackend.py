'''
port of youtube-dl's InfoExtractor for youtube
'''

from __future__ import absolute_import, unicode_literals

from .AbstractBackend import AbstractBackend
from ..exception import BackendFailedException
from ...urllib import request, parse, error
import re
import socket
import sys
import datetime
import logging
from ...htmlparser import parse as parsehtm


def clean_html(html):
    """Clean an HTML snippet into a readable string"""
    # Newline vs <br />
    html = html.replace('\n', ' ')
    html = re.sub('\s*<\s*br\s*/?\s*>\s*', '\n', html)
    # Strip html tags
    html = re.sub('<.*?>', '', html)
    return html


class YoutubeDLBackend(AbstractBackend):
    _VALID_URL = r'^((?:https?://)?(?:youtu\.be/|(?:\w+\.)?youtube(?:-nocookie)?\.com/|tube\.majestyc\.net/)(?!view_play_list|my_playlists|artist|playlist)(?:(?:(?:v|embed|e)/)|(?:(?:watch(?:_popup)?(?:\.php)?)?(?:\?|#!?)(?:.+&)?v=))?)?([0-9A-Za-z_-]+)(?(1).+)?$'
    _WEB_URL = 'http://www.youtube.com/watch?v=%s&gl=US&hl=en&has_verified=1'
    _INFO_URL = 'http://www.youtube.com/get_video_info?&video_id=%s%s&ps=default&eurl=&gl=US&hl=en'
    _SWF_RE = re.compile(r'swfConfig.*?"(http:\\/\\/.*?watch.*?-.*?\.swf)"')
    _DATE_RE = re.compile(r'id="eow-date.*?>(.*?)</span>', re.DOTALL)
    _NETRC_MACHINE = 'youtube'
    
    def _resolve(self):
        # Get video webpage
        #self.report_video_webpage_download(self.video_id)
        req = request.Request(self._WEB_URL % self.video_id)
        try:
            video_webpage = request.urlopen(req).read().decode("UTF-8")
        except (error.URLError, error.HTTPError, socket.error):
            err = sys.exc_info()[1]
            self.trouble('ERROR', 'unable to download video webpage: %s' \
                         % str(err))
            return

        # Attempt to extract SWF player URL
        mobj = self._SWF_RE.search(video_webpage)
        if mobj is not None:
            player_url = re.sub(r'\\(.)', r'\1', mobj.group(1))
        else:
            player_url = None

        # Get video info
        #self.report_video_info_webpage_download(video_id)
        for el_type in ['&el=embedded', '&el=detailpage', '&el=vevo', '']:
            video_info_url = (self._INFO_URL % (self.video_id, el_type))
            req = request.Request(video_info_url)
            try:
                video_info_webpage = request.urlopen(req).read().decode("utf8")
                video_info = parse.parse_qs(video_info_webpage)
                if 'token' in video_info:
                    break
            except (error.URLError, error.HTTPError, socket.error):
                err = sys.exc_info()[1]
                self.trouble('ERROR', 'unable to download video info webpage: %s'
                            % str(err))
                return
        
        if 'token' not in video_info:
            if 'reason' in video_info:
                self.trouble('ERROR', 'YouTube said: %s'
                             % video_info['reason'][0])
            else:
                self.trouble('ERROR', '"token" parameter not in video info for unknown reason')
            return

        # Check for "rental" videos
        if 'ypc_video_rental_bar_text' in video_info and \
                'author' not in video_info:
            self.trouble('ERROR', '"rental" videos not supported')
            return

        # Start extracting information
        #self.report_information_extraction(video_id)

        # uploader
        if 'author' not in video_info:
            self.trouble('ERROR', 'unable to extract uploader nickname')
            return
        video_uploader = parse.unquote_plus(video_info['author'][0])

        # title
        if 'title' not in video_info:
            self.trouble('ERROR', 'unable to extract video title')
            return
        video_title = parse.unquote_plus(video_info['title'][0])

        # thumbnail image
        if 'thumbnail_url' not in video_info:
            self.trouble('WARNING', 'unable to extract video thumbnail')
            video_thumbnail = ''
        else:    # don't panic if we can't find it
            video_thumbnail = parse.unquote_plus(video_info['thumbnail_url'][0])

        # upload date
        upload_date = 'NA'
        mobj = self._DATE_RE.search(video_webpage)
        if mobj is not None:
            upload_date = ' '.join(re.sub(r'[/,-]', r' ', mobj.group(1)).split())
            format_expressions = ['%d %B %Y', '%B %d %Y', '%b %d %Y']
            for expression in format_expressions:
                try:
                    upload_date = datetime.datetime.strptime(upload_date,
                                                expression).strftime('%Y%m%d')
                except:
                    pass

        # description
        markup = parsehtm(video_webpage)
        video_description = markup.getroot().get_element_by_id("eow-description").text
        if video_description:
            video_description = clean_html(video_description)
        else:
            video_description = ''

        # token
        video_token = parse.unquote_plus(video_info['token'][0])

        # Decide which formats to download
        if "url_encoded_fmt_stream_map" in video_info and \
                len(video_info["url_encoded_fmt_stream_map"]) >= 1:
            url_strs = video_info["url_encoded_fmt_stream_map"][0].split(",")
            url_datas = [parse.parse_qs(s) for s in url_strs]
            url_datas = filter(lambda d: "itag" in d and "url" in d, url_datas)
            url_map = dict([(int(d["itag"][0]),
                             "".join((d["url"][0], "&signature=", d["sig"][0])))
                            for d in url_datas])

        results = {
                   "fmt_url_map": url_map,
                   "video_id": self.video_id,
                   "title": video_title,
                   "description": video_description,
                   "token": video_token,
                   "thumbnail_url": video_thumbnail,
                   "player_url": player_url,
                   "uploader": video_uploader,
                   "fmt_list": url_map.keys(),
                   "fmt_stream_map": [dict([(k, v[0]) for k, v in d]) \
                                      for d in url_datas],
                   "date": upload_date,
                   }
        return results
    
    def trouble(self, level, reason):
        logging.getLogger("libyo.youtube.resolve.YoutubeDLBackend").log(getattr(logging, level), reason)
        if level == 'ERROR':
            raise BackendFailedException()
