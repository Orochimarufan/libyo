from abc import abstractmethod
from ...util.util import typeTriggerVar2, typeTriggerVar, setterFunc, yoObject

class AbstractProgressObject(yoObject):
    def __init__(self):
        #internal
        self._active=False
        self.stopIter=False
        self._isTaskList=False
        #Properties
        self.min=typeTriggerVar(self,"_i_min",int,self._f_ran)
        self.max=typeTriggerVar(self,"_i_max",int,self._f_ran,100)
        self._range(self.min,self.max)  #typeTriggerVar, in contrary to typeTriggerVar2 does not call the trigger for the init value
                                        #Why not use typeTriggerVar2 here, too? because _f_ran needs self.max and self.min to exist, which is not true while typeTriggerVar2 is run!
        self.position=typeTriggerVar2(self,"_i_pos",int,self._changed)
        self.task=typeTriggerVar2(self,"_s_task",str,self._task,"Processing...")
        self.name=typeTriggerVar2(self,"_s_name",str,self._name,"Progress")
        #set*()
        self.setMax=setterFunc(self,"max")
        self.setMin=setterFunc(self,"min")
        self.setPos=setterFunc(self,"position")
        self.setValue=setterFunc(self,"position")
        self.setName=setterFunc(self,"name")
        self.setTask=setterFunc(self,"task")
    def _f_ran(self,x):
        #typeTriggerVar only passes the changed value but _range needs min,max.
        self._range(self.min,self.max)
    def start(self):
        if not self._active:
            self._active=True
            self._start()
    def stop(self):
        if self._active:
            self._stop()
            self._active=False
    #convinience Methods
    def next(self,task=None):
        self.position+=1
        if self.position>self.max and self.stopIter:
            raise StopIteration()
        if self._isTaskList:
            self.task=self._taskList[self.position]
        elif task is not None:
            self.task=task
        return self.position
    def __iter__(self):
        self.stopIter=True
        return iter(self.next,StopIteration)
    def setup(self,name,task,minimum,maximum):
        self.min=minimum
        self.max=maximum
        self.position=0
        self.name=name
        self.task=task
        self._isTaskList=False
    def taskList(self,tasklist):
        self._taskList=[str(i) for i in tasklist]
        self.min=0
        self.max=len(self._taskList)-1
        self.position=0
        self.task=self._taskList[0]
        self._isTaskList=True
    def reset(self):
        self.min=0
        self.max=100
        self.position=0
        self.task="Processing..."
        self._isTaskList=False
    #Methods to override
    def _changed(self,position):
        if self._active:
            self._redraw()
    def _range(self,mini,maxi):
        if self._active:
            self._redraw()
    def _name(self,newname):
        if self._active:
            self._redraw()
    def _task(self,newtask):
        if self._active:
            self._redraw()
    #abstractmethods
    @abstractmethod
    def _start(self):
        raise NotImplementedError()
    @abstractmethod
    def _stop(self):
        raise NotImplementedError()
    @abstractmethod
    def _redraw(self):
        raise NotImplementedError()