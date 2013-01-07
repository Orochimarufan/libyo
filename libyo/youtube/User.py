"""
----------------------------------------------------------------------
- youtube.User: object that describes a youtube user
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

from .gdata import gdata
import logging


class User(object):
    logger = logging.getLogger("libyo.youtube.User")
    
    def __init__(self, username):
        self.username = username
        self.base = "users/{0}/".format(username)
    
    def _gdata(self, mod, params=None, ssl=True):
        return gdata(self.base + mod, params, ssl)
    
    def favorites_simple(self, start=1, results=25):
        return self._gdata("favorites", [("start-index", start), ("max-results", results)])
    
    def favorites_skeleton(self):
        return self.favorites_simple(1, 1)
    
    def favorites(self):
        skel = self.favorites_skeleton()
        got = 0
        pmax = skel["data"]["totalItems"]
        items = []
        while got < pmax:
            tmp = self.favorites_simple(got + 1, 50)
            if "items" not in tmp["data"]:
                self.logger.warn("Ran into a Wall while processing: FAV[{0}] MAX[{1}] GOT[{2}]; This needn't be bad, since YouTube may have 'flagged' some videos of your favorites.".format(self.username, pmax, got))
                break
            for i in tmp["data"]["items"]:
                items.append(i)
                got += 1
        skel["data"]["itemsPerPage"] = len(items)
        skel["data"]["items"] = items
        return skel
    
    def playlists(self):
        return self._gdata("playlists")
    
    def subscriptions(self):
        return self._gdata("subscriptions")
    
    def contacts(self):
        return self._gdata("contacts")
    
    def profile(self):
        return self._gdata("")
    
    def newsubvideos(self):
        return self._gdata("newsubscriptionvideos")
