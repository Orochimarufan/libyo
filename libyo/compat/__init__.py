"""
----------------------------------------------------------------------
- compat: Compatibility Package
----------------------------------------------------------------------
- Copyright (C) 2011-2013  Orochimarufan
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

import sys
import importlib
import logging
import platform

PY3 = sys.version_info >= (3,)
logging.getLogger(__name__).info("Running on {0} {1} {2}".format(
                                    platform.python_implementation(),
                                    ".".join(map(str, sys.version_info[:3])),
                                    sys.version_info[3]))
