"""
----------------------------------------------------------------------
- utils.jimport: java-style import function
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

import logging


def jimport(className, nameSpace=None):
    a = (className, className.split(".")[-1])
    b = "from {0} import {1}".format(*a)
    c = {}
    logging.getLogger(__name__).debug("'{0}'".format(className) + (" -> " + nameSpace.__name__ if nameSpace is not None else ""))
    exec (b, c) #@UndefinedVariable
    if nameSpace is not None:
        import types
        if isinstance(nameSpace, types.ModuleType):
            nameSpace.__dict__[a[1]] = c[a[1]]
        elif isinstance(nameSpace, type):
            setattr(nameSpace, a[1], c[a[1]])
        else:
            nameSpace[a[1]] = c[a[1]]
    return c[a[1]]
