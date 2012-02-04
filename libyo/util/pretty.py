'''
Created on 02.02.2012

@author: hinata
'''

def fillP(string,length,filler=" "):
    string=str(string)
    return "".join([filler*(length-len(string)),string])
def fillA(string,length,filler=" "):
    string=str(string)
    return "".join([string,filler*(length-len(string))])
