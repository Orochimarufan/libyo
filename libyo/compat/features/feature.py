"""
----------------------------------------------------------------------
- compat.features.feature: Feature Implementation Selection Mechanism
----------------------------------------------------------------------
- Copyright (C) 2011-2012  Orochimarufan
-                 Authors: Orochimarufan <orochimarufan.x3@gmail.com>
-
- This program is free software: you can redistribute it and/or modify
- it under the terms of the GNU General Public License as published by
- the Free Software Foundation, either version 3 of the License, or
- (at your option) any later version.
-
- This program is distributed in the hope that it will be useful,
- but WITHOUT ANY WARRANTY; without even the implied warranty of
- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
- GNU General Public License for more details.
-
- You should have received a copy of the GNU General Public License
- along with this program.  If not, see <http://www.gnu.org/licenses/>.
----------------------------------------------------------------------
"""

from __future__ import absolute_import, unicode_literals

import inspect
import logging


def CompatibilityFeature(name, IMPLS, module="libyo.compat.features"):
    import importlib as _import
    for n, p in IMPLS:
        try:
            MODULE = _import.import_module(p, module)
        except ImportError:
            continue
        else:
            IMPL = n
            break
    else:
        IMPL = False
    _set = inspect.currentframe().f_back.f_globals
    _set["IMPL"] = IMPL
    if not IMPL:
        raise ImportError("Could not Import any {0} Implementation!".format(name))
    _set["MODULE"] = MODULE
    if hasattr(MODULE, "__all__"):
        _iter = MODULE.__all__
    else:
        _iter = dir(MODULE)
    for i in _iter:
        _set[i] = getattr(MODULE, i)
    del _iter
    del _set

    logging.getLogger(module).info("{0} Implementation: {1}".format(name, IMPL))
