"""
----------------------------------------------------------------------
- util.choice: ArgumentParser style choices
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


#Case Insensitive choices
class cichoice(object):
    @staticmethod
    def unify(x):
        return str(x).lower()
    
    @classmethod
    def compare(self, one, two):
        return self.unify(one) == self.unify(two)
    
    @classmethod
    def new(cls, *args):
        return cls(args)
    
    @classmethod
    def from_dict(cls, dictionary):
        return cls(dictionary.keys())
    
    def __init__(self, choiceList):
        self.list = [self.unify(i) for i in choiceList]
        
    def __contains__(self, string):
        return self.unify(string) in self.list
    
    def __getitem__(self, index):
        return self.list.__getitem__(index)
    
    def __repr__(self):
        return "<Choices [" + ",".join(self.list) + "] at " + hex(id(self)) + ">"
    
    def __len__(self):
        return len(self.list)
    
    def add(self, string):
        self.list.append(self.unify(string))
        
    def remove(self, string):
        self.list.remove(self.unify(string))


class qchoice(cichoice):
    @staticmethod
    def unify(x):
        try:
            return int(str(x).lower().rstrip("p"))
        except ValueError:
            raise ValueError("qChoices: Quality values have to be a Number or Number+'p'! Not matching: " + str(x))


class switchchoice(list):
    def __contains__(self, other):
        return not [c for c in other if not list.__contains__(self, c)]

