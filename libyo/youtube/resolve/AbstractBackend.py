"""
----------------------------------------------------------------------
- youtube.resolve.AbstractBackend: abstract Resolver backend
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

from abc import abstractmethod
from ..exception import BackendFailedException
import logging


class AbstractBackend(object):
    def setup(self, video_id):
        self.video_id = video_id
    
    def resolve(self, video_id=None):
        if video_id is not None:
            self.setup(video_id)
        try:
            return self._resolve()
        except BackendFailedException as e:
            logging.debug("Error in Backend %s: %s" % (self.__class__.__name__, str(e)))
            return False
    
    @abstractmethod
    def _resolve(self):
        raise NotImplementedError()
