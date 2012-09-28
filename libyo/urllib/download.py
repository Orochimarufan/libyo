'''
Created on 01.12.2011

@author: hinata
'''
from .. import compat
from ..interface.progress import AbstractProgressObject
from ..util.util import mega
import os.path

urllib = compat.getModule("urllib");

def downloadProgress(remote,local,progress=None,mine=True,bytesize=32*1024):
    valid=isinstance(progress,AbstractProgressObject)
    length=int(remote.info().get("content-length",-1))
    if valid:
        if length==-1:
            if mine:
                    progress.name="Download"
                    progress.task="".join(["File: '",os.path.split(local.name)[-1],"' Size UNKNOWN"])
            if hasattr(progress,"unknown"):
                progress.unknown=True
            else:
                progress.max=100
                progress.position=99
                progress.min=0
            progress_unknown=True
        else:
            progress_unknown=False
            progress.max=length
            progress.position=0
            progress.min=0
            if mine==True:
                progress.name="Download"
                progress.task="".join(["File='",os.path.split(local.name)[-1],"'; Size='",mega(length,True),"'"])
            elif mine==2 or mine==3:
                progress.task=progress.task.replace("\x11",mega(length,True))
        progress.start()
    while True:
        recvd=remote.read(bytesize)
        if not recvd:
            break
        local.write(recvd)
        if valid:
            if length==-1:
                if progress_unknown:
                    progress.next()
            else:
                progress.position+=bytesize
    if valid and not mine==3:
        progress.stop()

def download(url,filename,progress=None,mine=True,bytesize=32*1024,to=0,ua=None):
    req = urllib.request.Request(url)
    if ua is not None:
        req.add_header("User-Agent", ua)
        req.add_header("Referer", "http://youtube.com")
    with urllib.request.urlopen(req) as remote:
        with open(filename,"wb") as local:
            return downloadProgress(remote,local,progress,mine,bytesize)

if __name__=="__main__":
    #from ..interface.progress.simple import SimpleProgress2
    #p=SimpleProgress2()
    from ..interface.progress.file import SimpleFileProgress
    p = SimpleFileProgress()
    import sys
    download(sys.argv[1],sys.argv[2],p)
