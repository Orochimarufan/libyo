'''
Created on 23.02.2012

@author: hinata
'''

from __future__ import absolute_import, unicode_literals, division

from .gdata import gdata
import logging

class User(object):
    logger = logging.getLogger("libyo.youtube.User")
    def __init__(self,username):
        self.username=username;
        self.base="users/{0}/".format(username);
    def _gdata(self,mod,params=None,ssl=True):
        return gdata(self.base+mod,params,ssl);
    def favorites_simple(self,start=1,results=25):
        return self._gdata("favorites",[("start-index",start),("max-results",results)]);
    def favorites_skeleton(self):
        return self.favorites_simple(1, 1);
    def favorites(self):
        skel = self.favorites_skeleton();
        got  = 0;
        pmax = skel["data"]["totalItems"];
        items= [];
        while got < pmax:
            tmp = self.favorites_simple(got+1, 50);
            if "items" not in tmp["data"]:
                self.logger.warn("Ran into a Wall while processing: FAV[{0}] MAX[{1}] GOT[{2}]; This needn't be bad, since YouTube may have 'flagged' some videos of your favorites.".format(self.username,pmax,got));
                break;
            for i in tmp["data"]["items"]:
                items.append(i);
                got+=1;
        skel["data"]["itemsPerPage"]=len(items)
        skel["data"]["items"]=items
        return skel
    def playlists(self):
        return self._gdata("playlists");
    def subscriptions(self):
        return self._gdata("subscriptions");
    def contacts(self):
        return self._gdata("contacts");
    def profile(self):
        return self._gdata("")
