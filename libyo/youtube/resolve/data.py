#!/usr/bin/python3

from __future__ import unicode_literals

class FMTValue(object):
    def __init__(self, fmt, c, vc, vp, vres, vbits, ac, abits, asr, ach):
        self.fmt = fmt
        self.container = c
        self.video_codec = vc[1]
        self.video_codec_long = vc[0]
        self.video_profile = vp
        self.video_resolution = vres
        self.video_bitrate = vbits
        self.audio_codec = ac[1]
        self.audio_codec_long = ac[0]
        self.audio_bitrate = abits
        self.audio_samplerate = asr
        self.audio_channels = ach
    def __str__(self):
        return self.format_caption()
    def format_caption(self,template="{video_res_progressive} {container}/{video_codec}"):
        return template.format(**self.__dict__,
                video_res_progressive = self.video_resolution.progressive,
                video_res_vga = self.video_resolution.vga,
                video_res_height = self.video_resolution.h,
                video_res_width = self.video_resolution.w)

class VideoResolution(object):
    def __init__(self,w,h,progressive,vga):
        self.progressive = progressive
        self.vga = vga
        self.w = w
        self.h = h
    def __str__(self):
        return "{0}x{1}".format(self.w,self.h)
    def __eq__(self,other):
        if isinstance(other,VideoResolution):
            if self.progressive == other.progressive or \
                self.vga == other.vga or \
                self.w == other.w and self.h == other.h:
                return True
            return False
        return NotImplemented

resolutions = {
        #Standard Resolutions
        240: VideoResolution(400,240,"240p","WQVGA"),
        270: VideoResolution(480,270,"270p","HVGA"),
        360: VideoResolution(640,360,"360p","nHD"),
        480: VideoResolution(854,480,"480p","FWVGA"),
        720: VideoResolution(1280,720,"720p","WXGA"),
        1080: VideoResolution(1920,1080,"1080p","WUXGA"),
        3072: VideoResolution(4096,3072,"3072p","HXGA"),
        #3D Resolutions
        "_240": VideoResolution(854,240,"240p",None),
        "_360": VideoResolution(640,360,"360p",None),
        "_520": VideoResolution(1920,520,"520p",None),
        "_720": VideoResolution(1280,720,"720p",None),
        #Mobile
        "3gp": VideoResolution(176,144,None,None)
        }

codecs = {
        "sorenson":("Sorenson H.263", "Spark"),
        "avc":("MPEG-4 AVC H.264", "AVC"),
        "vp8":("Google VP8", "VP8"),
        "mp3":("MPEG II Layer 3", "MP3"),
        "aac":("Advanced Audio Coding", "AAC"),
        "vorbis":("OGG Vorbis Audio", "Vorbis"),
        }

formats = [
        # Flash
        FMTValue(5,  "flv",codecs["sorenson"],None,resolutions[240],"250k",codecs["mp3"],"64k","22k",2),
        FMTValue(6,  "flv",codecs["sorenson"],None,resolutions[270],"800k",codecs["mp3"],"64k","22k",2),
        FMTValue(34, "flv",codecs["avc"],"Main",resolutions[360],"500k",codecs["aac"],"128k","44k",2),
        FMTValue(35, "flv",codecs["avc"],"Main",resolutions[480],"800-1000k",codecs["aac"],"128k","44k",2),
        # MP4
        FMTValue(18, "mp4",codecs["avc"],"Baseline",resolutions[360],"500k",codecs["aac"],"96k","44k",2),
        FMTValue(22, "mp4",codecs["avc"],"High",resolutions[720],"2-2.9M",codecs["aac"],"152k","44k",2),
        FMTValue(37, "mp4",codecs["avc"],"High",resolutions[1080],"3-4.3M",codecs["aac"],"152k","44k",2),
        FMTValue(38, "mp4",codecs["avc"],"High",resolutions[3072],"3.5-5M",codecs["aac"],"152k","44k",2),
        # WebM
        FMTValue(43, "webm",codecs["vp8"],None,resolutions[360],"500k", codecs["vorbis"],"128k","44k",2),
        FMTValue(44, "webm",codecs["vp8"],None,resolutions[480],"1000k",codecs["vorbis"],"128k","44k",2),
        FMTValue(45, "webm",codecs["vp8"],None,resolutions[720],"2000k",codecs["vorbis"],"192k","44k",2),
        FMTValue(46, "webm",codecs["vp8"],None,resolutions[1080],None,  codecs["vorbis"],"192k","44k",2),
        # MP4 3D
        FMTValue(83, "mp4",codecs["avc"],"3D",resolutions["_240"],"500k",codecs["aac"],"96k","44k",2),
        FMTValue(82, "mp4",codecs["avc"],"3D",resolutions["_360"],"500k",codecs["aac"],"96k","44k",2),
        FMTValue(85, "mp4",codecs["avc"],"3D",resolutions["_520"],"2-2.9M",codecs["aac"],"152k","44k",2),
        FMTValue(84, "mp4",codecs["avc"],"3D",resolutions["_720"],"2-2.9M",codecs["aac"],"159k","44k",2),
        # WebM 3D
        FMTValue(100,"webm",codecs["vp8"],"3D",resolutions["_360"],None,codecs["vorbis"],"128k","44k",2),
        FMTValue(101,"webm",codecs["vp8"],"3D",resolutions["_480"],None,codecs["vorbis"],"192k","44k",2),
        #FMTValue(46, "webm",codecs["vp8"],"3D",resolutions["_540"],None,codecs["vorbis"],"192k","44k",2),
        FMTValue(102,"webm",codecs["vp8"],"3D",resolutions["_720"],None,codecs["vorbis"],"192k","44k",2),
        # Mobile
        FMTValue(13, "3gp",codecs["mp4"],None,resolutions["3gp"],"500k",codecs["aac"],None,"22k",1),
        FMTValue(17, "3gp",codecs["mp4"],None,resolutions["3gp"],"2000k",codecs["aac"],None,"22k",1),
        ]

getFmtFormat = lambda fmt: [i for i in formats if i.fmt == fmt][0]
