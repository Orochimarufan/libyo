'''
Created on 01.12.2011

@author: hinata
'''

from __future__ import absolute_import, unicode_literals, division

from collections import OrderedDict as pod

profiles = pod((
            ("mixed-avc",(pod([(1080,37),(720,22),(719,45),(480,44),(360,18),(359,43),(240,5)]),"Use best (prefer MPEG4/AVC)")),
            ("mixed",(pod([(1080,37),(720,45),(480,44),(360,43),(240,5)]),"Use best (prefer WebM)")),
            ("webm",(pod([(720,45),(480,44),(360,43)]),"Use WebM only.")),
            ("avc",(pod([(1080,37),(720,22),(360,18)]),"Use MPEG4/AVC only.")),
            ("flash",(pod([(480,35),(360,34),(240,5)]),"Use FlashVideo only.")),
            ("mobile",({240:17},"Use YouTube Mobile (3GP/176x144)")),
            ("3d",(pod([(720,102),(480,101),(360,100),(240,83)]),"Use 3D (prefer WebM)")),
            ("3d-avc",(pod([(720,84),(480,101),(360,82),(240,83)]),"Use 3D (prefer MPEG4/AVC)")),
            ("avc-3d",(pod([(720,84),(520,85),(360,82),(240,83)]),"Use 3D with MPEG4/AVC")),
            ("webm-3d",(pod([(720,102),(540,46),(480,101),(360,100)]),"Use 3D with WebM")),
            ("mixed-3d",(pod([(720,102),(719,45),(480,101),(479,44),(360,100),(359,18),(240,83),(239,5)]),"Try to use 3D (perfer WebM)")),
            ("mixed-3d-avc",(pod([(720,84),(719,22),(480,101),(479,44),(360,82),(359,18),(240,83),(239,5)]),"Try to use 3D (prefer MPEG4/AVC"))
           ))

descriptions = pod((
            #Flash/FLV    [Sorenson Spark|MP3]
            (5,  "240p Flash/FLV"),
            (6,  "270p Flash/FLV"),
            #Flash/FLV    [Sorenson Spark|AAC]
            (34, "360p Flash/FLV"),
            (35, "480p Flash/FLV"),
            #WebM/VP8     [VP8|Vorbis]
            (43, "360p WebM/VP8"),
            (44, "480p WebM/VP8"),
            (45, "720p WebM/VP8"),
            #(46, "1080p WebM/VP8"), #XXX: DUP?
            #MPEG4/AVC    [H.264|AAC]
            (18, "360p MPEG4/AVC"),
            (22, "720p MPEG4/AVC"),
            (37, "1080p MPEG4/AVC"),
            (38, "Original MPEG4/AVC (2304p)"),
            #Mobile/3GP   [MPEG-4-Visual|AAC]
            (17, "176x144 Mobile/3GP"),
            #MPEG4/AVC 3D [H.264|AAC]
            (83, "240p MPEG4/AVC 3D"),
            (82, "360p MPEG4/AVC 3D"),
            (85, "520p MPEG4/AVC 3D"),
            (84, "720p MPEG4/AVC 3D"),
            #WebM/VP8 3D  [VP8|Vorbis]
            (100,"360p WebM/VP8 3D"),
            (101,"480p WebM/VP8 3D"),
            (46, "540p WebM/VP8 3D"), #XXX: DUP?
            (102,"720p WebM/VP8 3D")
           ))
file_extensions  = { #incomplete
    18: "mp4", 22: "mp4", 37: "mp4", 38: "mp4", 83: "mp4", 82: "mp4", 85: "mp4", 84: "mp4",
     5: "flv", 34: "flv", 35: "flv",
    43:"webm", 44:"webm", 45:"webm", 100:"webm", 101:"webm", 46:"webm", 102:"webm",
    17: "3gp"
}
