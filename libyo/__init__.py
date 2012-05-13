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

from __future__ import absolute_import, unicode_literals, division
import logging

DEBUG = True
if DEBUG:
    logging.basicConfig(level=logging.DEBUG)

LIBYO_VERSION_MAJOR=0
LIBYO_VERSION_MINOR=9
LIBYO_VERSION_MICRO=9
LIBYO_VERSION_PATCH="y"
__VERSION__=(LIBYO_VERSION_MAJOR,LIBYO_VERSION_MINOR,LIBYO_VERSION_MICRO,LIBYO_VERSION_PATCH);
LIBYO_VERSION="{0}.{1}.{2}{3}".format(*__VERSION__)

#moved comparison to version module
from .version import Version as _VersionClass

minVersion              = _VersionClass.LibyoVersion.minVersion
reqVersion              = _VersionClass.LibyoVersion.requireVersion
fancyReqVersion         = _VersionClass.LibyoVersion.fancyRequireVersion
LibyoOutdatedException  = _VersionClass.OutdatedError

logging.getLogger("libyo").info("Running LibYo Version {0}".format(_VersionClass.LibyoVersion.format()))
