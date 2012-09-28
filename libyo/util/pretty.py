'''
Created on 02.02.2012

@author: hinata
'''

from __future__ import unicode_literals, print_function

def fillP(string,length,filler=" "):
    string=str(string)
    return "".join([filler*(length-len(string)),string])
def fillA(string,length,filler=" "):
    string=str(string)
    return "".join([string,filler*(length-len(string))])

def prettyexc(header=None,notrace=False,ndash=60,**kargs):
    import traceback
    print("-"*ndash)
    if header:
        print(header)
    if notrace:
        import sys
        print("".join(traceback.format_exception_only(*sys.exc_info[:2],**kargs)),end="")
    else:
        traceback.print_exc(**kargs)
    print("-"*ndash)

