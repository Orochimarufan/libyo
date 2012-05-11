"""
@author Orochimarufan
@module libyo.xspf.XspfObject
@created 2011-12-12
@modified 2012-05-04
"""

from __future__ import absolute_import, unicode_literals, division

import logging
from ..compat import etree as ElementTree
from .XspfUtils import XspfUtils,_isUri
from .XspfTrackList import XspfTrackList
from .XspfTrack import XspfTrack
import datetime
from copy import copy
from ..util.File import File

class XspfObject(object):
    xmlns="http://xspf.org/ns/0/"
    xml  = None

    @classmethod
    def new(klass,sTitle=None,sCreator=None):
        self = klass()
        self.setTitle(sTitle)
        self.setCreator(sCreator)
        return self
    @classmethod
    def fromFile(klass,fp):
        fp = File(fp);
        re=klass.fromETree(ElementTree.parse(fp.fp)); #@UndefinedVariable
        fp.done();
        return re;
    @classmethod
    def fromETree(klass, etree):
        return klass.fromXml(etree.getroot())
    @classmethod
    def fromXml(klass, elem):
        tracks = XspfUtils.find(elem,"trackList")
        trackList = XspfTrackList()
        for track in tracks:
            trackList.append(XspfTrack(track))
        del elem[elem.index(tracks)]
        self = klass(etree=elem,trackList=trackList)
        return self
    def __init__(self,etree=None,trackList=None):
        if etree is None:
            self.xml   = ElementTree.Element("playlist",version="1",nsmap={None:self.xmlns}) #@UndefinedVariable
        elif etree.__class__ is ElementTree._Element: #@UndefinedVariable
            self.xml    = etree
        elif etree.__class__ is ElementTree._ElementTree: #@UndefinedVariable
            self.xml    = etree.getroot()
        self.setTitle=XspfUtils.setOrCreateElementTextHook2(self.xml, "title")
        self.getTitle=XspfUtils.getElementTextHook(self.xml, "title")
        self.setCreator=XspfUtils.setOrCreateElementTextHook2(self.xml, "creator")
        self.getCreator=XspfUtils.getElementTextHook(self.xml, "creator")
        self.setAnnotation=XspfUtils.setOrCreateElementTextHook2(self.xml, "annotation")
        self.getAnnotation=XspfUtils.getElementTextHook(self.xml, "annotation")
        self.setInfo=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "info", _isUri)
        self.getInfo=XspfUtils.getElementTextHook(self.xml, "info")
        self.setLocation=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "location", _isUri)
        self.getLocation=XspfUtils.getElementTextHook(self.xml, "location")
        self.setIdentifier=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "identifier", _isUri)
        self.getIdentifier=XspfUtils.getElementTextHook(self.xml, "identifier")
        self.setImage=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "image", _isUri)
        self.getImage=XspfUtils.getElementTextHook(self.xml, "image")
        def setDate(self,date):
            if date.__class__ is datetime.datetime:
                date    = date.isoformat()
            if date.__class__ is "".__class__:
                if not XspfUtils.validateDateTime(date):
                    raise ValueError("Invalid xsd:dateTime String. http://www.w3.org/TR/xmlschema-2/#dateTime")
            else:
                raise ValueError("'date' needs to be of Type datetime.datetime or String")
            XspfUtils.setOrCreateElementText(self.xml, "date", date)
        def getDate(self, asDatetime=False):
            if asDatetime:
                return XspfUtils.isoToDateTime(XspfUtils.getElementText(self.xml, "date"))
            else:
                return XspfUtils.getElementText(self.xml, "date")
        self.setDate = setDate.__get__(self)
        self.getDate = getDate.__get__(self)
        self.setLicense=XspfUtils.checkedSetOrCreateElementTextHook2(self.xml, "license", _isUri)
        self.getLicense=XspfUtils.getElementTextHook(self.xml, "license")
        #TODO: xml.playlist.attribution element (spec 4.1.1.2.10)
        #TODO: xml.playlist.link elements (spec 4.1.1.2.11)
        #TODO: xml.playlist.meta elements (spec 4.1.1.2.12)
        #TODO: xml.playlist.extension elements (spec 4.1.1.2.13)
        if trackList is None:
            self.trackList = XspfTrackList()
        else:
            self.trackList = trackList
    
    def addTrack(self,xspfTrack):
        if xspfTrack.__class__ is not XspfTrack:
            raise ValueError("'xspfTrack' must be of type XspfTrack. create one by calling XspfObject.newTrack()")
        self.trackList.append(xspfTrack)
    def getTrack(self,index):
        return self.trackList[index]
    def popTrack(self,index):
        return self.trackList.pop(index)
    def delTrack(self, xspfTrack):
        self.trackList.remove(xspfTrack)
    def newTrack(self,sTitle=None,sCreator=None,sLocation=None):
        return XspfTrack.new(sTitle,sCreator,sLocation)
    
    def toString(self,pretty_print=True,xml_declaration=False,encoding="utf8"):
        return ElementTree.tostring(self.toXml(),xml_declaration=xml_declaration,encoding=encoding,pretty_print=pretty_print) #@UndefinedVariable
    def toXml(self):
        xml = copy(self.xml)
        xml.append(self.trackList.toXml())
        return xml
    def toETree(self):
        return ElementTree.ElementTree(self.toXml()) #@UndefinedVariable
    def toFile(self, fp, encoding="utf8", method="xml", pretty_print=True, xml_declaration=True):
        fp = File(fp,"wb");
        self.toETree().write(fp.fp,encoding,method,pretty_print,xml_declaration);
        fp.done();
    def toFile_c14n(self, fp):
        fp = File(fp,"wb");
        self.toETree().write_c14n(fp.fp);
        fp.done();