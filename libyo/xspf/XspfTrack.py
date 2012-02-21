'''
Created on 12.12.2011

@author: hinata
'''
import lxml.etree
from .XspfUtils import XspfUtils,_isUri
def _isNNI(string):
    """Non-Negative Integer"""
    try:
        return int(string)>0
    except ValueError:
        return False

class XspfTrack(object):
    xml=None
    @classmethod
    def new(klass,sTitle,sCreator,sLocation):
        self = klass()
        self.setTitle(sTitle)
        self.setCreator(sCreator)
        if sLocation is not None:
            self.setLocation(sLocation)
        return self
    def __init__(self,elem=None):
        super(XspfTrack,self).__init__()
        if elem is None:
            self.xml = lxml.etree.Element("track") #@UndefinedVariable
        else:
            self.xml = elem
        #get/set Functions
        self.setLocation=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "location", _isUri)
        self.getLocation=XspfUtils.getElementTextHook(self.xml, "location")
        self.setIdentifier=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "identifier", _isUri)
        self.getIdentifier=XspfUtils.getElementTextHook(self.xml, "identifier")
        self.setTitle=XspfUtils.setOrCreateElementTextHook2(self.xml, "title")
        self.getTitle=XspfUtils.getElementTextHook(self.xml, "title")
        self.setCreator=XspfUtils.setOrCreateElementTextHook2(self.xml, "creator")
        self.getCreator=XspfUtils.getElementTextHook(self.xml, "creator")
        self.setAnnotation=XspfUtils.setOrCreateElementTextHook2(self.xml,"annotation")
        self.getAnnotation=XspfUtils.getElementTextHook(self.xml, "annotation")
        self.setInfo=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "info", _isUri)
        self.getInfo=XspfUtils.getElementTextHook(self.xml, "info")
        self.setImage=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "image", _isUri)
        self.getImage=XspfUtils.getElementTextHook(self.xml, "image")
        self.setAlbum=XspfUtils.setOrCreateElementTextHook2(self.xml, "album")
        self.getAlbum=XspfUtils.getElementTextHook(self.xml, "album")
        self.setTrackNum=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "trackNum", _isNNI)
        self.getTrackNum=XspfUtils.getElementTextHook(self.xml, "trackNum")
        self.setDuration=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "duration", _isNNI)
        self.getDuration=XspfUtils.getElementTextHook(self.xml, "duration")
        #TODO: xml.playlist.trackList.track.link element (spec 4.1.1.2.14.1.1.1.11)
        #TODO: xml.playlist.trackList.track.meta elements (spec 4.1.1.2.14.1.1.1.12)
        #TODO: xml.playlist.trackList.track.extension elements (spec 4.1.1.2.14.1.1.1.13)
    def toXml(self):
        return self.xml
    def toString(self):
        return lxml.etree.tostring(self.xml,pretty_print=True) #@UndefinedVariable