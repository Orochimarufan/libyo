'''
Created on 28.11.2011

@author: hinata
'''

import libyo.compat as _compat;
_urllib = _compat.getModule("urllib");
unicode_unescape = _compat.getModule("util").unicode_unescape;
unicode_escape = _compat.getModule("util").unicode_escape;
string_unescape = _compat.getModule("util").string_unescape;
string_escape = _compat.getModule("util").string_escape;
input = _compat.getModule("util").input; #@ReservedAssignment

def listreplace(lis,old,new):
    return [(i if i != old else new) for i in lis]
def listreplace_s(lis,old,new):
    return [i.replace(old,new) for i in lis]

def getkv(string, delim="=", unq=0):
    """turns string "key{delim}value" into tuple ("key","value").
    if UNQ AND UNQP are TRUE it will UrlUnQuote_Plus the value
    if UNQ BUT NOT UNQP is TRUE it will UrlUnQuote the value."""
    x = string.split(delim)
    if unq==1:
        return x[0],_urllib.parse.unquote_plus(x[1])
    elif unq==2:
        return x[0],_urllib.parse.unquote(x[1])
    else:
        return x

def sdict_parser(string,kvdelim="=",delim="&",unq=1):
    """Parse Strings:
    "a=b&b=c&k=v&key=value"
    
    Parameters:
        string: the string to parse
        kvdelim: the key/value delimiter (default="=")
        delim: the pair delimiter (default="&")
        unq: UrlUnquote values: 0=No 2=Yes 3=Plus"""
    return dict([getkv(i,kvdelim,unq) for i in string.split(delim)])

def mega(iIn,bStrOut=False,bBase10=False,sStrStr=" ",):
    if bBase10:
        base=1000;
    else:
        base=1024;
    table = {1024:["B","kiB","MiB","GiB","TiB"],
             1000:["B","kB", "MB", "GB", "TB"]}
    x=0;
    i=int(iIn);
    while i > base:
        x+=1;
        i=i/base;
        if x==len(table[base]):
            break;
    return ("{0:.2f}{1}{2}".format(round(i,2),sStrStr,table[base][x]) if bStrOut else (i,table[base][x]))

