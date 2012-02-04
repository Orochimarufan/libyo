'''
Created on 02.02.2012

@author: hinata
'''


class File(object):
    def __init__(self,fp,mode=None):
        if fp.__class__ is "".__class__:
            self.fp=open(fp,mode);
            self.fpc=True;
        else:
            self.fp=fp;
            self.fpc=False;
    def done(self):
        if self.fpc:
            self.fp.close();
        