"""
@author Orochimarufan
@module libyo.compat.etree
@created 2012-05-11
@modified 2012-05-11
"""

from __future__ import absolute_import, unicode_literals;
del absolute_import, unicode_literals
from .features import CompatibilityFeature

__all__ = ["parse","Element","ElementTree","_Element"]

IMPLS =  [
         ("LXML","lxml.etree"),
         ("CPYTHON","xml.etree.cElementTree"),
         ("PUREPYTHON","xml.etree.ElementTree"),
         ("elementtree","elementtree.ElementTree")
         ];

CompatibilityFeature("ElementTree",IMPLS)

del CompatibilityFeature,IMPLS