"""
----------------------------------------------------------------------
- youtube.resolve.MixBackend: mix multiple backends, taking the first that works
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
from __future__ import absolute_import, unicode_literals, division

from .AbstractBackend import AbstractBackend


class MixBackend(AbstractBackend):
    def __init__(self, *in_backends):
        self.backends = in_backends
        self.results = []
    
    def _resolve(self):
        for backend in self.backends:
            backend.setup(self.video_id)
            result = backend.resolve()
            if result:
                return result
        return False


class __MixBackend2(MixBackend):
    def _resolve(self):
        self.results = []
        for backend in self.backends:
            backend.setup(self.video_id)
            self.results.append(backend.resolve())
        mixed = dict()
        for result in self.results:
            if not result:
                continue
            for k, v in result.items():
                if k not in mixed:
                    mixed[k] = v
        return mixed
