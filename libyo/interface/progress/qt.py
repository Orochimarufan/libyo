"""
----------------------------------------------------------------------
- interface.progress.qt: Qt QProgressDialog Progress implementation
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

from .abstract import AbstractProgressObject
from PyQt4 import QtGui


class QtProgress(AbstractProgressObject):
    def __init__(self, dialog=None, parent=None):
        if dialog is None:
            self.dialog = QtGui.QProgressDialog(parent)
        else:
            self.dialog = dialog
        #The Dialog has to be set-up BEFORE AbstractProgressObject.__init__() is called!
        super(QtProgress, self).__init__()
        self.dialog.setAutoClose(False)
        self.dialog.setAutoReset(False)
        self.dialog.close() #we dont want the window initially
    
    def _changed(self, iPos):
        self.dialog.setValue(iPos)
    
    def _range(self, iMin, iMax):
        self.dialog.setRange(iMin, iMax)
    
    def _name(self, sName):
        self.dialog.setWindowTitle(sName)
    
    def _task(self, sTask):
        self.dialog.setLabelText(sTask)
    
    def _start(self):
        self.dialog.show()
    
    def _stop(self):
        self.dialog.close()
    
    def _redraw(self):
        pass #everything is handled above
    
    def reset(self):
        self.dialog.reset()
        super(QtProgress, self).reset()
    
    def setup(self, sName, sTask, iMin, iMax):
        self.dialog.reset()
        super(QtProgress, self).setup(sName, sTask, iMin, iMax)
