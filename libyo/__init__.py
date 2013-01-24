"""
----------------------------------------------------------------------
- libyo: Orochimarufan's shared code library
----------------------------------------------------------------------
- Copyright (C) 2011-2013  Orochimarufan
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
Features:
    libyo.caching - defines a Type that features Expiring items
    libyo.magic - use Linux magic to determine filetypes.
    libyo.youtube.resolve - resolve YouTube Videos
    libyo.youtube.Playlist - retrive YouTube playlists
    libyo.configparser - StdPy configparser extension
    libyo.xspf - Stuff for handling xspf playlists - not complete
    libyo.argparse - StdPy ArgumentParser extension
    libyo.interface - user interface code
    libyo.extern - code written by other people
    libyo.compat - some compatibility code
    libyo.reflect - reflection code
    libyo.urllib - urllib(2) extensions
"""
from __future__ import absolute_import, unicode_literals

from collections import namedtuple
ntup = namedtuple("version_info", "major,minor,micro,patch")

# -------------------------------------------------
# libyo version
version_info = ntup(0, 10, 0, 0)
version = "0.10"
# -------------------------------------------------


# -------------------------------------------------
# Auto-logging:
#  if not run with python -O, and the logging module
#  is not already imported, set it up to echo INFO
import sys
if __debug__ and "logging" not in sys.modules:
    import logging
    logging.basicConfig(level=logging.INFO)
# -------------------------------------------------


# -------------------------------------------------
# Generate Int Version
hexversion = int("{0:02X}{1:02X}{2:03X}{3:04X}".format(*version_info), 16)

# Legacy
__VERSION__ = tuple(version_info)
LIBYO_VERSION = ".".join(map(str, version_info))
LIBYO_VERSION_MAJOR, \
LIBYO_VERSION_MINOR, \
LIBYO_VERSION_PATCH = version_info[:3]

# Echo Version
import logging
logging.getLogger("libyo").info("libyo version {0}".format(version))
# -------------------------------------------------

# clean module dict
del logging, sys
ntup.__repr__ = ntup.__str__ = ntup.__unicode__ =\
lambda self: "libyo.version_info(major=%i, minor=%i, micro=%i, patch=%i)" % self
del namedtuple, ntup
del absolute_import, unicode_literals
