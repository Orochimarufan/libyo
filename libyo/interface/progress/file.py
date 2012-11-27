# (c) 2012 Orochimarufan

import sys
import math
import operator
import time
import re
import functools
import collections
from . import AbstractProgressObject
from ...extern.terminal import getTerminalSize
from ...util.pretty import fillP
from ...util.util import mega
from ...util.reflect import TypeVar, TypeTriggerVar2
from .simple import SimpleProgress2

tft = ["s","min","h"]
lft = 3
def mytime(secs):
    d = 0
    while secs>60 and d<lft:
        d   += 1
        secs = secs // 60
    return "".join([str(int(secs)),tft[d]])
#mytime = lambda s: str(int(s))+"s"

class SCC(collections.deque):
    def __init__(self,max=25):
        self.max=max
    def put(self,f):
        self.append(f)
        if len(self)>self.max:
            self.popleft()
    def avg(self):
        return sum(self)/len(self)

class SimpleFileProgress(SimpleProgress2):
    _components         = { "{bar}":        0b00000001,
                            "{percent}":    0b00000010,
                            "{speed}":      0b00000100,
                            "{eta}":        0b00001000,
                            "{total}":      0b00010000,
                            "{title}":      0b00100000,
                            "{task}":       0b01000000,
                            "{position}":   0b10000000 }
    _extVars            = re.compile("\{[^\}]*\}")
    _defaultformat      = "{position}/{total} {bar} {percent} {speed} ETA: {eta}"
    
    def __init__(self, format=None, base10=False):
        super(SimpleFileProgress,self).__init__()
        self.format = TypeTriggerVar2(str, self._newformat, format or self._defaultformat)
        self.base10=base10
        self._iLastTime = time.time()
        self._iLastPos = 0
        self.override = False
        self._oAvgSpeed = SCC()
    
    def setupfile(self, name, length):
        self.setup(name,"",0,length)
    
    def _newformat(self, format):
        """ Called when format gets changed. """
        self._iFormatLen = len(self._extVars.sub("",format))
        self._iFormatCom = 0
        for k,t in self._components.items():
            if k in format:
                self._iFormatCom |= t
        self._redrawMaybe()
    
    def _range(self,iMin,iMax):
        """ Called when min or max get changed. """
        self._sTotal    = mega(iMax,True,self.base10,"")
        self._iTotalLen = len(self._sTotal)
        self._redrawMaybe()
    
    def _name(self,sName):
        """ Called when Title changes """
        self._iTitleLen = len(sName)
        self._redrawMaybe()
    
    def _task(self,sTask):
        """ Called when Task Name changes """
        self._iTaskLen = len(sTask)
        self._redrawMaybe()
    
    def _redrawMaybe(self):
        """ Redraw only if we are supposed to be. """
        if self._active:
            self._redraw()
    
    def _doSpeedCalc(self):
        iCTime  = time.time()
        iCPos   = self.position
        iDTime  = iCTime - self._iLastTime
        iDPos   = iCPos - self._iLastPos
        self._iSpeed    = iDPos // iDTime
        self._iLastTime = iCTime
        self._iLastPos  = iCPos
        self._oAvgSpeed.put(self._iSpeed)
        self._iAvgSpeed = self._oAvgSpeed.avg()
    
    def _doEta(self):
        """ Format ETA
        Run after _doSpeedCalc()!"""
        if self._iAvgSpeed>0:
            self._iEta      = (self.max - self.position) / self._iAvgSpeed
            self._sEta      = mytime(self._iEta)
        else:
            #self._iEta      = -1
            self._sEta      = "---"
        self._iEtaLen   = len(self._sEta)
    
    def _redraw_known(self):
        """ Redraw when the percentage is known. """
        iSpace = getTerminalSize()[0] - self._iFormatLen
        dFdict = dict()
        
        if self._iFormatCom & 16: #total
            dFdict ["total"] = self._sTotal
            iSpace -= self._iTotalLen
        if self._iFormatCom & 32: #title
            dFdict ["title"] = self.name
            iSpace -= self._iTitleLen
        if self._iFormatCom & 64: #task
            dFdict ["task"] = self.task
            iSpace -= self._iTaskLen
        if self._iFormatCom & 128: #position
            sPos   = mega(self.position,True,self.base10,"")
            dFdict ["position"] = sPos
            iSpace -= len(sPos)
        if self._iFormatCom & 2: #percent
            sPer   = "".join([str(round(self.position/self.max*100,1)),"%"])
            dFdict ["percent"] = sPer
            iSpace -= len(sPer)
        #Speed and ETA
        s = self._iFormatCom & 4
        e = self._iFormatCom & 8
        if s or e:
            self._doSpeedCalc()
        if s:
            sSpeed = "".join([mega(self._iSpeed,True,self.base10,""),"/s"])
            dFdict ["speed"] = sSpeed
            iSpace -= len(sSpeed)
        if e:
            self._doEta()
            dFdict ["eta"] = self._sEta
            iSpace -= self._iEtaLen
        #Bar
        if self._iFormatCom & 1:
            iTiles = iSpace-2
            iArrow = int(math.floor( self.position * ( iTiles / self.max ) ))
            sBar   = "".join(["[","="*(iArrow-1),">" if iArrow>0 else ""," "*(iTiles-iArrow),"]"]) #progress bar magic ;)
            dFdict ["bar"] = sBar
            iSpace -= len(sBar)
        
        if iSpace<0 and not self.override:
            sys.stdout.write("Format is too Long (%i) or Terminal is not wide enough! (%i%%)\r"%(abs(iSpace)+getTerminalSize()[0],round(self.position/self.max*100,1)))
        else:
            sys.stdout.write("".join([self.format.format(**dFdict),"\r"]))
            
