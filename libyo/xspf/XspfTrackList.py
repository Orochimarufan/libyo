'''
Created on 12.12.2011

@author: hinata
'''
import lxml.etree 

class XspfTrackList(list):
    def toXml(self):
        xml = lxml.etree.Element("trackList") #@UndefinedVariable
        for track in self:
            xml.append(track.toXml())
        return xml
    def toString(self):
        return lxml.etree.tostring(self.toXml(),pretty_print=True) #@UndefinedVariable