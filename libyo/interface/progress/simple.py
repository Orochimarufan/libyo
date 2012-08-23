'''
Created on 01.12.2011

@author: hinata
'''
import sys
import math
from . import AbstractProgressObject
from ...extern.terminal import getTerminalSize
from ...util.pretty import fillP
from ...util.reflect import TypeVar

class SimpleProgress(AbstractProgressObject):
    def _start(self):
        self._redraw()
    def _stop(self):
        sys.stdout.write("\n")
    def _redraw(self):
        self._colums=getTerminalSize()[0]
        perc=fillP(round(self.position/self.max*100,1),5)
        text="{0}: {1} [{2}%]".format(self.name,self.task,perc)
        sys.stdout.write("".join([text," "*(self._colums-len(text)),"\r"]))

class SimpleProgress2(SimpleProgress):
    def __init__(self):
        super(SimpleProgress2,self).__init__()
        self.unknown=TypeVar(bool,False)
        self._r_lastpos=0
        self._r_backwards=False
    def _redraw(self):
        if self.unknown:
            self._redraw_unknown()
        else:
            self._redraw_known()
    def _redraw_common(self):
        self._colums=getTerminalSize()[0]
        self._r_text="{name}: {task}".format(name=self.name,task=self.task)
        self._r_space=self._colums-(len(self._r_text)+10)
    def _redraw_known(self):
        self._redraw_common()
        tiles=self._r_space/self.max
        marke=math.floor(self.position*tiles)
        prbar="".join(["[","="*(marke-1),(">" if marke>0 else "")," "*(self._r_space-marke),"]"])
        perce=fillP(round(self.position/self.max*100,1),5)
        sys.stdout.write("{0} {1} {2}%\r".format(self._r_text,prbar,perce))
    def _redraw_unknown(self):
        self._redraw_common()
        if self._r_backwards:
            marke=self._r_lastpos-math.ceil(self._r_space/50)
        else:
            marke=self._r_lastpos+math.ceil(self._r_space/50)
        if marke >= self._r_space:
            self._r_backwards=True
            marke=self._r_space-2
        elif marke <= 1:
            self._r_backwards=False
            marke=1
        prbar="".join(["["," "*(marke-1),"<=>"," "*(self._r_space-marke-2),"]"])
        self._r_lastpos=marke
        sys.stdout.write("{0} {1}\r".format(self._r_text,prbar))

