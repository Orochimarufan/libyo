"""
----------------------------------------------------------------------
- xspf.XspfTrack: a single Track in a XSPF playlist
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

from ..compat import etree as ElementTree

from .XspfUtils import XspfUtils, _isUri


def _isNNI(string):
    """Non-Negative Integer"""
    try:
        return int(string) > 0
    except ValueError:
        return False


class XspfTrack(object):
    xml = None
    
    @classmethod
    def new(klass, sTitle, sCreator, sLocation):
        self = klass()
        self.setTitle(sTitle)
        self.setCreator(sCreator)
        if sLocation is not None:
            self.setLocation(sLocation)
        return self
    
    def __init__(self, elem=None):
        super(XspfTrack, self).__init__()
        if elem is None:
            self.xml = ElementTree.Element("track") #@UndefinedVariable
        else:
            self.xml = elem
        #get/set Functions
        self.setLocation = XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "location", _isUri)
        self.getLocation = XspfUtils.getElementTextHook(self.xml, "location")
        self.setIdentifier = XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "identifier", _isUri)
        self.getIdentifier = XspfUtils.getElementTextHook(self.xml, "identifier")
        self.setTitle = XspfUtils.setOrCreateElementTextHook2(self.xml, "title")
        self.getTitle = XspfUtils.getElementTextHook(self.xml, "title")
        self.setCreator = XspfUtils.setOrCreateElementTextHook2(self.xml, "creator")
        self.getCreator = XspfUtils.getElementTextHook(self.xml, "creator")
        self.setAnnotation = XspfUtils.setOrCreateElementTextHook2(self.xml, "annotation")
        self.getAnnotation = XspfUtils.getElementTextHook(self.xml, "annotation")
        self.setInfo = XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "info", _isUri)
        self.getInfo = XspfUtils.getElementTextHook(self.xml, "info")
        self.setImage = XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "image", _isUri)
        self.getImage = XspfUtils.getElementTextHook(self.xml, "image")
        self.setAlbum = XspfUtils.setOrCreateElementTextHook2(self.xml, "album")
        self.getAlbum = XspfUtils.getElementTextHook(self.xml, "album")
        self.setTrackNum = XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "trackNum", _isNNI)
        self.getTrackNum = XspfUtils.getElementTextHook(self.xml, "trackNum")
        self.setDuration = XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "duration", _isNNI)
        self.getDuration = XspfUtils.getElementTextHook(self.xml, "duration")
        #TODO: xml.playlist.trackList.track.link element (spec 4.1.1.2.14.1.1.1.11)
        #TODO: xml.playlist.trackList.track.meta elements (spec 4.1.1.2.14.1.1.1.12)
        #TODO: xml.playlist.trackList.track.extension elements (spec 4.1.1.2.14.1.1.1.13)
    
    def toXml(self):
        return self.xml
    
    def toString(self):
        return ElementTree.tostring(self.xml,pretty_print=True) #@UndefinedVariable
