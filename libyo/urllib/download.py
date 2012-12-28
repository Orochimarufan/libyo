"""
----------------------------------------------------------------------
- urllib.download: file download functions using urllib
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
from __future__ import absolute_import, unicode_literals

from ..interface.progress.abstract import AbstractProgressObject
from ..util.util import mega
import os.path
from . import request

BS = 32 * 1024


def downloadProgress(remote, local, progress=None, mine=True, bytesize=BS):
    valid = isinstance(progress, AbstractProgressObject)
    length = int(remote.info().get("content-length", -1))
    if (valid):
        if (length == -1):
            if (mine):
                    progress.name = "Download"
                    progress.task = "".join(["File: '",
                            os.path.split(local.name)[-1], "' Size UNKNOWN"])
            if (hasattr(progress, "unknown")):
                progress.unknown = True
            else:
                progress.max = 100
                progress.position = 99
                progress.min = 0
            progress_unknown = True
        else:
            progress_unknown = False
            progress.max = length
            progress.position = 0
            progress.min = 0
            if (mine == True):
                progress.name = "Download"
                progress.task = "".join(["File='", os.path.split(local.name)[-1],
                        "'; Size='", mega(length, True), "'"])
            elif (mine == 2 or mine == 3):
                progress.task = progress.task.replace("\x11", mega(length, True))
        progress.start()
    while (True):
        recvd = remote.read(bytesize)
        if (not recvd):
            break
        local.write(recvd)
        if (valid):
            if (length == -1):
                if (progress_unknown):
                    progress.next()
            else:
                progress.position += bytesize
    if (valid and not mine == 3):
        progress.stop()


def download(url, filename, progress=None, mine=True, bytesize=BS, to=0, ua=None):
    req = request.Request(url)
    if (ua is not None):
        req.add_header("User-Agent", ua)
        req.add_header("Referer", "http://youtube.com")
    with request.urlopen(req) as remote:
        with open(filename, "wb") as local:
            return downloadProgress(remote, local, progress, mine, bytesize)


if (__name__ == "__main__"):
    #from ..interface.progress.simple import SimpleProgress2
    #p=SimpleProgress2()
    from ..interface.progress.file import SimpleFileProgress
    p = SimpleFileProgress()
    import sys
    download(sys.argv[1], sys.argv[2], p)
