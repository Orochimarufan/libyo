'''
Created on 10.12.2011

@author: hinata
'''
from . import AbstractProgressObject
from PyQt4 import QtGui

class QtProgress(AbstractProgressObject):
    def __init__(self,dialog=None,parent=None):
        if dialog is None:
            self.dialog=QtGui.QProgressDialog(parent)
        else:
            self.dialog=dialog
        #The Dialog has to be set-up BEFORE AbstractProgressObject.__init__() is called!
        super(QtProgress,self).__init__()
        self.dialog.setAutoClose(False)
        self.dialog.setAutoReset(False)
        self.dialog.close() #we dont want the window initially
    def _changed(self,iPos):
        self.dialog.setValue(iPos)
    def _range(self,iMin,iMax):
        self.dialog.setRange(iMin,iMax)
    def _name(self,sName):
        self.dialog.setWindowTitle(sName)
    def _task(self,sTask):
        self.dialog.setLabelText(sTask)
    def _start(self):
        self.dialog.show()
    def _stop(self):
        self.dialog.close()
    def _redraw(self):
        pass #everything is handled above
    def reset(self):
        self.dialog.reset()
        super(QtProgress,self).reset()
    def setup(self,sName,sTask,iMin,iMax):
        self.dialog.reset()
        super(QtProgress,self).setup(sName,sTask,iMin,iMax)