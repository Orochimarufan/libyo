#!/usr/bin/python3

from __future__ import absolute_import, division, unicode_literals

try:
    from lxml import etree as etree
except ImportError:
    try:
        from xml.etree import cElementTree as etree
    except ImportError:
        from xml.etree import ElementTree as etree

from ..compat import getModule as _gm
urlopen = _gm("urllib.request").urlopen
entities = _gm("html").entities
from ..compat.uni import unichr
import math
import re

html_refex = re.compile(r'&(?:(#)(\d+)|([^;]+));')
def html_reflacer(match):
    if match.group(1):
        return unichr(int(match.group(2)))
    else:
        return unichr(entities.name2codepoint[match.group(3)])
html_decode = lambda s: html_refex.sub(html_reflacer, s)


def getTracks(videoId):
    document = etree.parse(urlopen("http://video.google.com/timedtext?type=list&v="+videoId))
    transcript_list = document.getroot()
    tracks = []
    for track in transcript_list:
        ti = int(track.get("id"))
        na = track.get("name")
        ln = track.get("lang_code")
        lo = track.get("lang_original")
        lt = track.get("lang_translated")
        ld = bool(track.get("lang_default"))
        tracks.append(SubtitleTrack(videoId,ti,na,ln,lo,lt,ld))
    return tracks

class SubtitleTrack(object):
    def __init__(self,vi,ti,na,ln,lo,lt,ld):
        self.videoId = vi
        self.trackId = ti
        self.name = na
        self.lang = ln
        self.lang_original = lo
        self.lang_translated = lt
        self.lang_default = ld
        self.xml = None
        self.srt = None
    def getURL(self):
        return "http://video.google.com/timedtext?type=track&v={0}&name={1}&lang={2}".format(self.videoId,self.name,self.lang)
    def getXML(self):
        if not self.xml:
            self.xml = etree.parse(urlopen(self.getURL()))
        return self.xml
    def getSRT(self):
        if not self.srt:
            self.srt = ""
            document = self.getXML()
            i = 0
            for line in document.getroot():
                i+=1
                self.srt+=self._srt_makeEntry(i,float(line.get("start")),float(line.get("dur")),line.text)
        return self.srt
    @staticmethod
    def _srt_makeEntry(n,start,duration,text):
        nms,nsec = math.modf(start)
        nmin = math.floor(nsec/60); nsec = nsec%60
        nhr = math.floor(nmin/60); nmin = nmin%60
        ems,esec = math.modf(start+duration)
        emin = math.floor(esec/60); esec = esec%60
        ehr = math.floor(emin/60); emin = emin%60
        caption = html_decode(text)
        return r"""{n}
{nhr:02.0f}:{nmin:02.0f}:{nsec:02.0f},{nms:03.0f} --> {ehr:02.0f}:{emin:02.0f}:{esec:02.0f},{ems:03.0f}
{caption}

""".format(**locals())
