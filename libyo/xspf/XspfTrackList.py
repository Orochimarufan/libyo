"""
@author Orochimarufan
@module libyo.xspf.XspfTrackList
@created 2011-12-12
@modified 2012-05-04
"""

from __future__ import absolute_import, unicode_literals, division

import lxml.etree 

class XspfTrackList(list):
    def toXml(self):
        xml = lxml.etree.Element("trackList") #@UndefinedVariable
        for track in self:
            xml.append(track.toXml())
        return xml
    def toString(self):
        return lxml.etree.tostring(self.toXml(),pretty_print=True) #@UndefinedVariable