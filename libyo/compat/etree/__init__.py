"""
@author Orochimarufan
@module libyo.compat.etree
@created 2012-05-11
@modified 2012-05-11
"""

from __future__ import absolute_import as _absimp, unicode_literals as _unilit;

IMPLS = {
         "LXML":"lxml.etree",
         "CPYTHON":"xml.etree.cElementTree",
         "PUREPYTHON":"xml.etree.ElementTree",
         "elementtree":"elementtree.ElementTree"
         };

import importlib as _import;

for n,p in IMPLS.items():
    try:
        MODULE = _import.import_module(p,"libyo.compat.etree");
    except ImportError:
        continue;
    else:
        IMPL = n;
        break;
else:
    IMPL = False;
    raise ImportError("Could not Import any ElementTree Implementation!");

if hasattr(MODULE,"__all__"):
    _iter = MODULE.__all__;
else:
    _iter = dir(MODULE)
_set = globals()
for i in _iter:
    _set[i] = getattr(MODULE,i)

del _set,_iter