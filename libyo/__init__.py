"""
libyo

(c) 2011-2012 by Orochimarufan/Hinata-chan [aka hinata]

Features:
    libyo.caching - defines a Type that features Expiring items
    libyo.magic - use Linux magic to determine filetypes.
    libyo.youtube.resolve - resolve YouTube Videos
    libyo.youtube.Playlist - retreive YouTube playlists
    libyo.configparser - StdPy configparser extension
    libyo.xspf - Stuff for handling xspf playlists - not complete
    libyo.argparse - StdPy ArgumentParser extension
    libyo.version - Version Handling code
    libyo.interface - user interface code
    libyo.extern - code written by other people
    libyo.compat - compatibility code
    libyo.reflect - reflection code
    libyo.urllib - urllib(2) extensions
"""

from __future__ import absolute_import, unicode_literals, division

__VERSION__ = "0.9.12"

import sys
if __debug__:
    if "logging" not in sys.modules:
        import logging
        logging.basicConfig(level=logging.INFO)

LIBYO_VERSION = tuple(map(int,__VERSION__.split(".")))
LIBYO_VERSION_MAJOR, LIBYO_VERSION_MINOR, LIBYO_VERSION_PATCH = LIBYO_VERSION[:3]

import logging
logging.getLogger("libyo").info("Running LibYo Version {0}".format(__VERSION__))

