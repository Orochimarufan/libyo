"""
@author Orochimarufan
@module libyo.compat.features
@created 2012-05-12
@modified 2012-05-12
"""

from __future__ import absolute_import, unicode_literals, division

from .. import PY3

import inspect
import logging
logger = logging.getLogger("libyo.compat.features")

def CompatibilityFeature(name,IMPLS):
    import importlib as _import;
    for n,p in IMPLS:
        try:
            MODULE = _import.import_module(p,"libyo.compat.features");
        except ImportError:
            continue;
        else:
            IMPL = n;
            break;
    else:
        IMPL = False;
    _set = inspect.currentframe().f_back.f_globals
    _set["IMPL"] = IMPL
    if not IMPL:
        raise ImportError("Could not Import any {0} Implementation!".format(name));
    _set["MODULE"] = MODULE
    if hasattr(MODULE,"__all__"):
        _iter = MODULE.__all__;
    else:
        _iter = dir(MODULE)
    for i in _iter:
        _set[i] = getattr(MODULE,i)
    del _iter
    del _set

    logger.info("{0} Implementation: {1}".format(name,IMPL))