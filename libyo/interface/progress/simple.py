"""
----------------------------------------------------------------------
- interface.progress.simple: Simple Terminal progress bar implementation
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

import sys
import math
from .abstract import AbstractProgressObject
from ...extern.terminal import getTerminalSize
from ...util.pretty import fillP
from ...util.reflect import TypeVar2


class SimpleProgress(AbstractProgressObject):
    def __init__(self, stream=sys.stdout):
        super(SimpleProgress, self).__init__()
        self.stream = stream
    
    def _start(self):
        self._redraw()
    
    def _stop(self):
        sys.stdout.write("\n")
    
    def _redraw(self):
        self._colums = getTerminalSize()[0]
        perc = fillP(round(self.position / self.max * 100, 1), 5)
        text = "{0}: {1} [{2}%]".format(self.name, self.task, perc)
        self.stream.write("".join([text, " " * (self._colums - len(text)), "\r"]))


class SimpleProgress2(SimpleProgress):
    unknown = TypeVar2(bool, False)
    
    def __init__(self, stream=sys.stdout):
        super(SimpleProgress2, self).__init__(stream)
        self._r_lastpos = 0
        self._r_backwards = False
    
    def _redraw(self):
        if self.unknown:
            self._redraw_unknown()
        else:
            self._redraw_known()
    
    def _redraw_common(self):
        self._colums = getTerminalSize()[0]
        self._r_text = "{name}: {task}".format(name=self.name, task=self.task)
        self._r_space = self._colums - (len(self._r_text) + 10)
    
    def _redraw_known(self):
        self._redraw_common()
        tiles = self._r_space / self.max
        marke = math.floor(self.position * tiles)
        prbar = "".join(["[",
                         "=" * (marke - 1),
                         ">" if marke > 0 else "",
                         " " * (self._r_space - marke),
                         "]"])
        perce = fillP(round(self.position / self.max * 100, 1), 5)
        self.stream.write("{0} {1} {2}%\r".format(self._r_text, prbar, perce))
    
    def _redraw_unknown(self):
        self._redraw_common()
        if self._r_backwards:
            marke = self._r_lastpos - math.ceil(self._r_space / 50)
        else:
            marke = self._r_lastpos + math.ceil(self._r_space / 50)
        if marke >= self._r_space:
            self._r_backwards = True
            marke = self._r_space - 2
        elif marke <= 1:
            self._r_backwards = False
            marke = 1
        prbar = "".join(["[", " " * (marke - 1), "<=>",
                         " " * (self._r_space - marke - 2), "]"])
        self._r_lastpos = marke
        self.stream.write("{0} {1}\r".format(self._r_text, prbar))
