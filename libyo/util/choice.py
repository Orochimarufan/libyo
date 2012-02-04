'''
Created on 01.02.2012

@author: hinata
'''

#Case Insensitive choices
class cichoice(object):
    @staticmethod
    def unify(x):
        return str(x).lower()
    @classmethod
    def compare(self,one,two):
        return self.unify(one)==self.unify(two)
    @classmethod
    def new(cls,*args):
        return cls(args)
    @classmethod
    def from_dict(cls,dictionary):
        return cls(dictionary.keys())
    def __init__(self,choiceList):
        self.list=[ self.unify(i) for i in choiceList ]
    def __contains__(self,string):
        return self.unify(string) in self.list
    def __getitem__(self,index):
        return self.list.__getitem__(index)
    def __repr__(self):
        return "<Choices ["+",".join(self.list)+"] at "+hex(self.id)+">"
    def __len__(self):
        return len(self.list)
    def add(self,string):
        self.list.append(self.unify(string))
    def remove(self,string):
        self.list.remove(self.unify(string))

class qchoice(cichoice):
    @staticmethod
    def unify(x):
        try:
            return int(str(x).lower().rstrip("p"))
        except ValueError:
            raise ValueError("qChoices: Quality values have to be a Number or Number+'p'! Not matching: "+str(x))

class switchchoice(list):
    def __contains__(self,other):
        return not [c for c in other if not list.__contains__(self,c)];
