'''
Created on 01.12.2011

@author: hinata
'''
from .. import compat
from ..user.progress import AbstractProgressObject
from ..util.util import mega
import os.path

urllib = compat.getModule("urllib");

def download(url,filename,progress=None,mine=True,bytes=32*1024):
    valid=isinstance(progress,AbstractProgressObject)
    with urllib.request.urlopen(url) as remote:
        length=int(remote.info().get("content-length",-1))
        if valid:
            if length==-1:
                if mine:
                        progress.name="Download"
                        progress.task="".join(["File: '",os.path.split(filename)[-1],"' Size UNKNOWN"])
                if hasattr(progress,"unknown"):
                    progress.unknown=True
                else:
                    progress.max=100
                    progress.position=99
                    progress.min=0
            else:
                progress.max=length
                progress.position=0
                progress.min=0
                if mine==True:
                    progress.name="Download"
                    progress.task="".join(["File='",os.path.split(filename)[-1],"'; Size='",mega(length,True),"'"])
                elif mine==2 or mine==3:
                    progress.task=progress.task.replace("\x11",mega(length,True))
        with open(filename,"wb") as local:
            if valid:
                progress.start()
            while True:
                recvd=remote.read(bytes)
                if not recvd:
                    break
                local.write(recvd)
                if valid:
                    if length==-1:
                        progress.next()
                    else:
                        progress.position+=bytes
            if valid and not mine==3:
                progress.stop()

if __name__=="__main__":
    from ..user.progress.simple import SimpleProgress2
    p=SimpleProgress2()
    import sys
    download(sys.argv[0],sys.argv[1],p)