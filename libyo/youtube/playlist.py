'''
Created on 28.11.2011

@author: hinata
'''

from .gdata import gdata
import logging
logger=logging.getLogger("libyo.youtube.playlist")

def simple      ( playlist_id, params=None ):
    return gdata("playlists/{}".format(playlist_id), params)

def skeleton    (playlist_id):
    return simple(playlist_id,[("max-results",1)])

def advanced    ( playlist_id ):
    skel= simple(playlist_id, [("max-results",1)])
    got = 0
    pos = 0
    pmax = skel["data"]["totalItems"]
    items= []
    while got < pmax:
        tmp=simple(playlist_id, [("max-results",50),("start-index",pos+1)])
        if "items" not in tmp["data"]:
            logger.warn("Ran into a Wall while processing: PL[{}] MAX[{}] GOT[{}] POS[{}]; This needn't be bad, since YouTube may have 'flagged' some videos of your playlist.".format(playlist_id,pmax,got,pos))
            break
        for i in tmp["data"]["items"]:
            got+=1
            if i["position"]>pos:
                pos=i["position"]
            items.append(i)
    skel["data"]["itemsPerPage"]=len(items)
    skel["data"]["items"]=items
    return skel

try:
    import lxml.html
    from ..compat import urlopen
    from .gdata import html_decode
    def noapi       (playlist_id):
        page=urlopen("http://youtube.com/playlist?list="+playlist_id)
        layout={"data":
                {"description":"",
                 "title": None,
                 "items": [],
                 "itemsPerPage":0,
                 "id":playlist_id,
                 "content":{"5":"http://www.youtube.com/p/"+playlist_id},
                 "startIndex":1,
                 "author":None,
                 "totalItems":0,
                 "thumbnail":{}
                 } ,"apiVersion":"libyo-youtube-playlist-noapi/1.0"}
        document=lxml.html.parse(page).getroot()
        window=document.find_class("playlist-info")[0]
        layout["title"]=html_decode(window.find_class("playlist-reference")[0][0].text)
        layout["author"]=html_decode(window.find_class("channel-author-attribution")[0][0].text)
        window=document.find_class("playlist-landing")[0]
        items=window.find_class("playlist-video-item")
        for item in items:
            item_layout={"position":int(item.find_class("video-index")[0].text),
                         "video":{
                                  "uploaded":"",
                                  "category":"",
                                  "updated":"",
                                  "rating":"",
                                  "description":"",
                                  "title":html_decode(item.find_class("video-title")[0].text),
                                  "tags":[],
                                  "thumbnail":{"hqDefault":item.find_class("video-thumb")[0][0][0].get("src")},
                                  "content":[],
                                  "player":[],
                                  "accessControl":{"comment":"allowed","list":"allowed","videoRespond":"moderated","rate":"allowed","syndicate":"allowed","embed":"allowed","commentVote":"allowed","autoPlay":"allowed"},
                                  "uploader":None,
                                  "ratingCount":0,
                                  "duration:":0,
                                  "commentCount":0,
                                  "likeCount":0,
                                  "favoriteCount":0,
                                  "id":None,
                                  "viewCount":0},
                         "id":"",
                         "author":layout["author"]}
            try:
                item_layout["video"]["id"]=item.find_class("yt-uix-button")[0].get("data-video-ids")
            except IndexError:
                item_layout["video"]["id"]=""
            try:
                item_layout["video"]["uploader"]=html_decode(item.find_class("video-owner")[0][0].text)
            except IndexError:
                item_layout["video"]["uploader"]=""
            layout["data"]["items"].append(item_layout)
        return layout
    def mixed       (playlist_id):
        api=advanced(playlist_id)
        def k(i):
            return int(i["position"])
        api["data"]["items"].sort(key=k)
        web=noapi(playlist_id)
        has=[i["position"] for i in api["data"]["items"]]
        has_id=[i["video"]["id"] for i in api["data"]["items"]]
        for i in web["data"]["items"]:
            if i["video"]["id"] not in has_id:
                api["data"]["items"].append(i)
                has.append(i["position"])
                has_id.append(i["video"]["id"])
        api["data"]["items"].sort(key=k)
        for i in range(len(api["data"]["items"])-1):
            api["data"]["items"][i]["position"]=i+1
        return api
except ImportError:
    pass