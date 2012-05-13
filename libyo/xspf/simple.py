"""
@author Orochimarufan
@module libyo.
@created 2012-
@modified 2012-
"""

from __future__ import absolute_import, unicode_literals, division

import xml.dom.minidom

from ..compat.uni import isstring

def dom_TextElement(tag,text):
    t = xml.dom.minidom.Text()
    t.data=text
    e = xml.dom.minidom.Element(tag)
    e.appendChild(t)
    return e

def dom_appendTextNode(node,tag,text):
    node.appendChild(dom_TextElement(tag,text))

class Track(object):
    def __init__(self,title,creator=None,album=None,uri=None,info=None,image=None,annotation=None):
        self.title = title
        self.creator = creator
        self.album = album
        self.uri = uri
        self.info = info
        self.image = image
        self.annotation = annotation
    def xml(self):
        track = xml.dom.minidom.Element("track")
        dom_appendTextNode(track,"title",self.title)
        if self.creator is not None:
            dom_appendTextNode(track,"creator",self.creator)
        if self.album is not None:
            pass #TODO: Album
        if self.uri is not None:
            dom_appendTextNode(track,"location",self.uri)
        if self.info is not None:
            dom_appendTextNode(track,"info",self.info)
        if self.image is not None:
            dom_appendTextNode(track,"image",self.image)
        if self.annotation is not None:
            dom_appendTextNode(track,"annotation",self.annotation)
        return track

class Playlist(list):
    def __init__(self,name,creator=None,tracks=[]):
        super(Playlist,self).__init__(tracks)
        self.name = name
        self.creator = creator
    def xml(self):
        document = xml.dom.minidom.getDOMImplementation().createDocument(None,"playlist",None)
        document.firstChild.setAttribute("xmlns","http://xspf.org/ns/0/")
        document.firstChild.setAttribute("version","1")
        dom_appendTextNode(document.firstChild,"title",self.name)
        if self.creator is not None:
            pass #TODO: playlist creator
        trackList = xml.dom.minidom.Element("trackList")
        for track in self:
            trackList.appendChild(track.xml())
        document.firstChild.appendChild(trackList)
        return document
    def __setitem__(self,index,value):
        if not isinstance(value,Track):
            raise ValueError("Playlist can only contain Tracks")
    def write(self,file):
        if isstring(file):
            with open(file,"w") as fp:
                self.xml().writexml(fp,"","","",encoding="UTF-8")
        else:
            self.xml().writexml(file,"","","",encoding="UTF-8")
