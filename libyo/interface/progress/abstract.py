"""
----------------------------------------------------------------------
- interface.progress.abstract: progress bar interface
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

from abc import abstractmethod
from ...util.reflect import TypeTriggerVar3, SetterDescriptor


class AbstractProgressObject(object):
    def __init__(self):
        #internal
        self._active = False
        self.stopIter = False
        self._isTaskList = False
        
        self.task = "Processing..."
        self.name = "Progress"
    
    def setRange(self, mini, maxi):
        type(self).min.notrigger(self, mini)
        self.max = maxi
    
    def _f_ran(self, x=None):
        self._range(self.min, self.max)
    
    def start(self):
        if not self._active:
            self._active = True
            self._start()
    
    def stop(self):
        if (self._active):
            self._stop()
            self._active = False
    
    #convenience Methods
    def next(self, task=None): #@ReservedAssignment
        self.position += 1
        if self.position > self.max and self.stopIter:
            raise StopIteration()
        if self._isTaskList:
            self.task = self._taskList[self.position]
        elif task is not None:
            self.task = task
        return self.position
    
    def __iter__(self):
        self.stopIter = True
        return iter(self.next, StopIteration)
    
    def setup(self, name, task, minimum, maximum):
        self.min = minimum
        self.max = maximum
        self.position = 0
        self.name = name
        self.task = task
        self._isTaskList = False
    
    def taskList(self, tasklist):
        self._taskList = [str(i) for i in tasklist]
        self.min = 0
        self.max = len(self._taskList) - 1
        self.position = 0
        self.task = self._taskList[0]
        self._isTaskList = True
    
    def reset(self):
        self.min = 0
        self.max = 100
        self.position = 0
        self.task = "Processing..."
        self._isTaskList = False
    
    #aliases
    done = stop
    nextTask = next
    
    #Methods to override
    def _changed(self, position):
        if self._active:
            self._redraw()
    
    def _range(self, mini, maxi):
        if self._active:
            self._redraw()
    
    def _name(self, newname):
        if self._active:
            self._redraw()
    
    def _task(self, newtask):
        if self._active:
            self._redraw()
    
    # attributes and setters
    min = TypeTriggerVar3(int, _f_ran, 0)
    max = TypeTriggerVar3(int, _f_ran, 100)
    position = TypeTriggerVar3(int, _changed, 0)
    task = TypeTriggerVar3(str, _task)
    name = TypeTriggerVar3(str, _name)
    
    setMax = SetterDescriptor("max")
    setMin = SetterDescriptor("min")
    setPos = SetterDescriptor("position")
    setValue = setPos
    setName = SetterDescriptor("name")
    setTask = SetterDescriptor("task")
    
    #abstract methods
    @abstractmethod
    def _start(self):
        raise NotImplementedError()
    
    @abstractmethod
    def _stop(self):
        raise NotImplementedError()
    
    @abstractmethod
    def _redraw(self):
        raise NotImplementedError()

