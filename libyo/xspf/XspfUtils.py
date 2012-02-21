'''
Created on 12.12.2011

@author: hinata
'''
from .. import compat
str = compat.getModule("util").unistr #@ReservedAssignment
import lxml.etree
import re
import datetime

import logging
from ..extern.UriRegex import HAS_REGEX as HAS_URI_REGEX
if not HAS_URI_REGEX:
    logging.getLogger("libyo.xspf.XspfUtils").warning("Cannot use UriRegex class. Elements that must be URIs will not be checked for Validity!")
    def _isUri(*args,**kwds):
        return True
else:
    from ..extern.UriRegex import UriRegex as _UriRegex
    _isUri = _UriRegex.getInstance().isUri

class XspfUtils(object):
    REG_DATETIME=re.compile("^\-?(?P<year>[0-9]{4,5})\-(?P<month>[0-1][0-9])\-(?P<day>[0-3][0-9])T(?P<hour>[0-2][0-9])\:(?P<minute>[0-5][0-9])\:(?P<second>[0-5][0-9])(?:\.(?P<fractional>[0-9]{2,8}))?(?P<zone>(?:[\+\-][0-1][0-9]\:[0-5][0-9])|Z)?$")
    REG_TIMEZONE=re.compile("(?:[\+\-](?P<hours>[0-1][0-9])\:(?P<minutes>[0-5][0-9]))|(?P<Z>Z)")
    XMLNS=None
    #To overcome the find problem
    @classmethod
    def makeTagName(cls,tag):
        from .XspfObject import XspfObject
        cls.XMLNS=XspfObject.xmlns
        def makeTagName(cls,tag):
            return "{{{0}}}{1}".format(cls.XMLNS,tag)
        cls.makeTagName=makeTagName.__get__(cls)
        return "{{{0}}}{1}".format(cls.XMLNS,tag)
    @classmethod
    def find(cls,node,tag):
        return node.find(cls.makeTagName(tag))
    
    #Low-Level XML Hooks
    @classmethod
    def appendTextElement(cls,node,tag,text):
        if text is None:
            return
        element     = lxml.etree.Element(cls.makeTagName(tag)) #@UndefinedVariable
        element.text= str(text)
        node.append(element)
        return element
    @classmethod
    def hasTag(cls,node,tag):
        return node.find(cls.makeTagName(tag)) is not None
    @classmethod
    def setElementText(cls,node,tag,text):
        e = node.find(cls.makeTagName(tag))
        e.text=text
        return e
    
    #High-Level XML Hooks
    @classmethod
    def setOrCreateElementText(cls,node,tag,text):
        if not XspfUtils.hasTag(node,tag):
            return XspfUtils.appendTextElement(node, tag, text)
        else:
            return XspfUtils.setElementText(node, tag, text)
    @classmethod
    def getElementText(cls,node,tag):
        if not cls.hasTag(node, tag):
            return None
        else:
            return node.find(tag).text
    
    #DateTime handlers
    @staticmethod
    def validateDateTime(string):
        x = XspfUtils.REG_DATETIME.match(string)
        if not x:
            return False
        try:
            datetime.datetime(2000,int(x.group("month")),
                              #Year does not get checked, because the xsd:dateTime spec does not have the limitations that python's datetime has.
                              int(x.group("day")),int(x.group("hour")),
                              int(x.group("minute")),int(x.group("second")))
        except ValueError:
            return False
        if "zone" in x.groupdict():
            z = XspfUtils.REG_TIMEZONE.match(x.group("zone"))
            if not z:
                return False
            if "Z" not  in z.groupdict():
                y = True
                y = y and int(z.group("hours")) in range(15)
                y = y and int(z.group("minutes")) in range(60)
                y = y and (int(z.group("hours")) < 14 or z.group("minutes")=="00")
                if not y:
                    return False
        return True
    @staticmethod
    def isoToDateTime(string):
        #wont check for validity, will only generate naive dateTime object (ignoring TZ info of the string)
        x = XspfUtils.REG_DATETIME.match(string)
        return datetime.datetime(int(x.group("year")),int(x.group("month")),
                                 int(x.group("day")),int(x.group("hour")),
                                 int(x.group("minute")),int(x.group("second")))
    
    #Hook Generators
    @staticmethod
    def getElementTextHook(node,tag):
        def f():
            return XspfUtils.getElementText(node,tag)
        return f
    @staticmethod
    def setOrCreateElementTextHook(node,tag):
        def f(text):
            return XspfUtils.setOrCreateElementText(node, tag, text)
        return f
    @staticmethod
    def setOrCreateElementTextHook2(node,tag):
        def f(text):
            XspfUtils.setOrCreateElementText(node, tag, text)
        return f
    @staticmethod
    def checkedSetOrCreateElementTextHook2(node, tag, checker):
        def f(text):
            if checker(text):
                XspfUtils.setOrCreateElementText(node, tag, text)
            else:
                raise ValueError("Value has to return True in: {0}\nDescription:\n{1}".format(repr(checker),checker.__doc__))
        return f