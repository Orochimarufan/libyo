"""
----------------------------------------------------------------------
- youtube.exception: Exception definitions
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

from ..base import LibyoError


class YouTubeException(LibyoError):
    pass


class YouTubeResolveError(YouTubeException):
    def __init__(self, msg, video_id, video_title=None):
        self.video_id = video_id
        self.video_title = (video_title if video_title is not None else "")
        if msg is None:
            msg = "could not resolve video: " + video_id
        super(YouTubeException, self).__init__(msg)


class FMTNotAvailableError(YouTubeResolveError):
    def __init__(self, video_id, fmt_requested, available_fmts=None,
                  title=None):
        msg = "FMT {0} not avaiable for Video with ID {1}".format(
                                                    fmt_requested, video_id)
        if available_fmts is not None:
            msg = "".join(msg, "\r\nAvaiable FMTs: ")
            msg = "".join(msg, ", ".join([str(x) for x in available_fmts]))
        super(YouTubeResolveError, self).__init__(msg, video_id, title)
        self.requested_fmt = fmt_requested
        self.available_fmt = (available_fmts if available_fmts is not None else [])


class BackendFailedException(YouTubeException):
    pass
