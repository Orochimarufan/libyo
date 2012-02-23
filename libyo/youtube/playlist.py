'''
Created on 28.11.2011

@author: hinata
'''

#this is a backport-wrapper of the Playlist class.

from .Playlist import Playlist

def simple      (playlist_id, params=None):
    return Playlist(playlist_id)._simple(params)

def skeleton    (playlist_id):
    return Playlist(playlist_id).skeleton()

def advanced    (playlist_id):
    return Playlist(playlist_id).advanced()

if Playlist.HAS_LXML:
    def noapi       (playlist_id):
        return Playlist(playlist_id).noapi()
    
    def mixed       (playlist_id):
        return Playlist(playlist_id).mixed()
