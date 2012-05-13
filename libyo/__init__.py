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
import logging

DEBUG = False#True
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

LIBYO_VERSION_MAJOR=0
LIBYO_VERSION_MINOR=9
LIBYO_VERSION_MICRO=10
LIBYO_VERSION_PATCH=""
__VERSION__=(LIBYO_VERSION_MAJOR,LIBYO_VERSION_MINOR,LIBYO_VERSION_MICRO,LIBYO_VERSION_PATCH);
LIBYO_VERSION="{0}.{1}.{2}{3}".format(*__VERSION__)

#moved comparison to version module
from .version import Version as _VersionClass

minVersion              = _VersionClass.LibyoVersion.minVersion
reqVersion              = _VersionClass.LibyoVersion.requireVersion
fancyReqVersion         = _VersionClass.LibyoVersion.fancyRequireVersion
LibyoOutdatedException  = _VersionClass.OutdatedError

logging.getLogger("libyo").info("Running LibYo Version {0}".format(_VersionClass.LibyoVersion.format()))
