"""
@author Orochimarufan
@module libyo.compat.etree
@created 2012-05-11
@modified 2012-05-11
"""

from __future__ import absolute_import as _absimp, unicode_literals as _unilit;

from ..util.switch import switch

import weakref

IMPLS =  [
         ("LXML","lxml.etree"),
         #("CPYTHON","xml.etree.cElementTree"), #wont work
         #("PUREPYTHON","xml.etree.ElementTree"),
         #("elementtree","elementtree.ElementTree")
         ];

from .features import CompatibilityFeature

CompatibilityFeature("ElementTree",IMPLS) #ImportError if lxml is missing

_set = globals()

with switch(IMPL) as case:
    if case("CPYTHON"):
        #we need _Element to be the Element class
        _set["_Element"]=type(MODULE.Element("a"))
    if case("PUREPYTHON"):
        # As with _Element, _ElementTree is the ETree class
        _set["_ElementTree"]=MODULE.ElementTree
        #Enable c14n
        import xml.etree.ElementTree as _pyetree
        from libyo.extern.ElementC14N import _serialize_c14n as _ser_c14n
        if "c14n" not in _pyetree._serialize:
            _pyetree._serialize["c14n"]=_ser_c14n;
        # ElementTree.Element.__init__
        _set["_PyElementFactory"]=MODULE.Element
        assert _PyElementFactory
        def Element(_tag, attrib=None, nsmap=None, **_extra):
            if attrib is None:
                attrib={}
            e = _PyElementFactory(_tag,attrib,**_extra)
            return e
        _set["Element"]=Element
        # ElementTree.ElementTree.write_c14n
        def write_c14n(etree,file):
            r = etree.getroot()
            dns=None
            etree.write(file,default_namespace=dns,method="c14n")
        _ElementTree.write_c14n=write_c14n

del _set,CompatibilityFeature