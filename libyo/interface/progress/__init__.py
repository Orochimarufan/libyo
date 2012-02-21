from abc import abstractmethod
from ...util.reflect import DescriptorObject, TypeTriggerVar2, TypeTriggerVar, setterFunc

class AbstractProgressObject(DescriptorObject):
    def __init__(self):
        super(AbstractProgressObject,self).__init__()
        #internal
        self._active=False
        self.stopIter=False
        self._isTaskList=False
        #descriptor vars
        self.min=TypeTriggerVar(int,self._f_ran)
        self.max=TypeTriggerVar(int,self._f_ran,100)
        self.position=TypeTriggerVar2(int,self._changed)
        self.task=TypeTriggerVar2(str,self._task,"Processing...")
        self.name=TypeTriggerVar2(str,self._name,"Progress")
        #set*()
        self.setMax=self.setMaximum=setterFunc(self,"max")
        self.setMin=self.setMinimum=setterFunc(self,"min")
        self.setPos=self.setPosition=\
        self.setValue=self.setCurrent=setterFunc(self,"position")
        self.setName=setterFunc(self,"name")
        self.setTask=setterFunc(self,"task")
    def setRange(self,mini,maxi):
        self.__getdescriptor__('min').notrigger(mini);
        self.__getdescriptor__('max').notrigger(maxi);
        self._f_ran();
    def _f_ran(self,x=None):
        self._range(self.min,self.max)
    def start(self):
        if not self._active:
            self._active=True
            self._start()
    def stop(self):
        if self._active:
            self._stop()
            self._active=False
    #convenience Methods
    def next(self,task=None): #@ReservedAssignment
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
    #aliases
    done=stop;
    nextTask=next;
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
