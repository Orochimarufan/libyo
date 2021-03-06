"""
----------------------------------------------------------------------
- youtube.resolve.CacheBackend: caches resolved video urls
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

from ...caching import Cache
from .AbstractBackend import AbstractBackend
from datetime import timedelta


class CacheBackend(AbstractBackend):
    def __init__(self, backend):
        self.backend = backend
        self.cache = Cache(default_duration=timedelta(minutes=10))
    
    def clear(self):
        self.cache.clear()
    
    def _resolve(self):
        if self.video_id not in self.cache:
            self.backend.setup(self.video_id)
            result = self.backend.resolve()
            self.cache.store(self.video_id, result)
            return result
        else:
            return self.cache.retreive(self.video_id)
