"""
----------------------------------------------------------------------
- reflect.property: property stuff
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

property = property


class classproperty(property):
    def __get__(self, inst, klass):
        if klass is None:
            klass = type(inst)
        if isinstance(self.fget, classmethod):
            return self.fget.__get__(inst, klass)()
        return self.fget(klass)
