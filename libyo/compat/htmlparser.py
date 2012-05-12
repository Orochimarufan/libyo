"""
@author Orochimarufan
@module libyo.compat.htmlparser
@created 2012-05-12
@modified 2012-05-12
"""

from __future__ import absolute_import, unicode_literals, division

from . import PY3
from .features import CompatibilityFeature

CompatibilityFeature("htmlparser",
                     [
                      ("lxml","lxml.html"),
                      ("fallback",".htmlparser_fallback")
                     ]
                    )
