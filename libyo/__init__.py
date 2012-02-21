"""
libyo

(c) 2011-2012 by Orochimarufan/Hinata-chan [aka hinata]

Features:
    libyo.caching - defines a Type that features Expiring items
    libyo.magic - use Linux magic to determine filetypes.
    libyo.youtube.resolve - resolve YouTube Videos
    libyo.youtube.playlist - retreive YouTube playlists
    libyo.configparser - StdPy configparser extension
    libyo.type - PreservedOrderDict: a dict-like type that preserves the order items were added
"""

LIBYO_VERSION_MAJOR=0
LIBYO_VERSION_MINOR=9
LIBYO_VERSION_PATCH=6
LIBYO_VERSION_MPATCH="b"
LIBYO_VERSION="{LIBYO_VERSION_MAJOR}.{LIBYO_VERSION_MINOR}.{LIBYO_VERSION_PATCH}{LIBYO_VERSION_MPATCH}".format(**locals())

def minVersion(major,minor=0,patch=0,mpatch=""):
    mpatch=str(mpatch).lower();
    return (LIBYO_VERSION_MAJOR,LIBYO_VERSION_MINOR,LIBYO_VERSION_PATCH,LIBYO_VERSION_MPATCH)\
               >=(major,minor,patch,mpatch);