"""
----------------------------------------------------------------------
- utils.File: File handling helper
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


class File(object):
    def __init__(self, fp, mode=None):
        if fp.__class__ is "".__class__:
            self.fp = open(fp, mode)
            self.fpc = True
        else:
            self.fp = fp
            self.fpc = False
    
    def done(self):
        if self.fpc:
            self.fp.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc, etype, f):
        self.done()
