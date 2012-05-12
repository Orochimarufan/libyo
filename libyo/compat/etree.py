"""
@author Orochimarufan
@module libyo.compat.etree
@created 2012-05-11
@modified 2012-05-11
"""

from __future__ import absolute_import as _absimp, unicode_literals as _unilit;

from ..util.switch import switch

IMPLS =  [
         ("LXML","lxml.etree"),
         ("CPYTHON","xml.etree.cElementTree"),
         ("PUREPYTHON","xml.etree.ElementTree"),
         ("elementtree","elementtree.ElementTree")
         ];

from .features import CompatibilityFeature

CompatibilityFeature("ElementTree",IMPLS)

_set = globals()

with switch(IMPL) as case:
    if case("CPYTHON"):
        #we need _Element to be the Element class
        _set["_Element"]=type(MODULE.Element("a"))
    if case("PUREPYTHON"):
        #Enable c14n
        import xml.etree.ElementTree as _pyetree
        from libyo.extern.ElementC14N import _serialize_c14n as _ser_c14n
        if "c14n" not in _pyetree._serialize:
            _pyetree._serialize["c14n"]=_ser_c14n;
        # As with _Element, _ElementTree is the ETree class
        _set["_ElementTree"]=MODULE.ElementTree

del _set,CompatibilityFeature