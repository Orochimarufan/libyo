"""
----------------------------------------------------------------------
- utils.Stack: stack operation module
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
- All operations are implemented as properties, as they don't take args
- add numbers to the stack with the += operator
----------------------------------------------------------------------
"""
from __future__ import absolute_import, unicode_literals, division

import collections


class Stack(collections.deque):
    """A FORTH-Style Stack Object"""
    # Property-style implementations of collection.deque methods
    @property
    def rotate(self):
        super(Stack, self).rotate(self.pop)
    
    @property
    def pop(self):
        return super(Stack, self).pop()
    
    @property
    def take(self):
        self.dup
        return self.pop
    
    # FORTH stack operators
    @property
    def dup(self):
        a = self.pop
        self += a
        self += a
    
    @property
    def drop(self):
        self.pop
    
    @property
    def swap(self):
        self += 1
        self.rotate
        a = self.pop
        self += -1
        self.rotate
        self += a
    
    @property
    def over(self):
        self.swap
        self.dup
        a = self.pop
        self.swap
        self += a
    
    @property
    def rot(self):
        self += 1
        self.rotate
        self.swap
        self += -1
        self.rotate
        self.swap
    
    @property
    def rot2(self):
        self.rot
        self.rot
    
    @property
    def nip(self):
        self.swap
        self.drop
    
    @property
    def tuck(self):
        self.swap
        self.over
    
    @property
    def pick(self):
        self.dup
        n = self.pop
        self.rotate
        self.dup
        a = self.pop
        self += -n
        self.rotate
        self += a
    
    @property
    def roll(self):
        self.dup
        n = self.pop
        self.rotate
        a = self.pop
        self += -n
        self.rotate
        self += a
    
    # 2-cell Stack Opertaors
    @property
    def ddup(self):
        self.over
        self.over
    
    @property
    def ddrop(self):
        self.drop
        self.drop
    
    @property
    def dswap(self):
        self.rot
        a = self.pop
        self.rot
        self += a
    
    @property
    def dover(self):
        self.rot
        a = self.pop
        self.rot
        b = self.take
        self.rot2
        self += a
        self.rot2
        self += b
        self += a
    
    @property
    def dnip(self):
        self.dswap
        self.ddrop
    
    @property
    def dtuck(self):
        self.dswap
        self.dover
    
    @property
    def drot(self):
        self += 2
        self.rotate
        self.dswap
        self += -2
        self.rotate
        self.dswap
    
    @property
    def drot2(self):
        self.drot
        self.drot
    
    # Operators
    @property
    def add(self):
        self += self.pop + self.pop
    
    @property
    def sub(self):
        self += self.pop - self.pop
    
    @property
    def mul(self):
        self += self.pop * self.pop
    
    @property
    def div(self):
        self += self.pop / self.pop
    
    @property
    def equal(self):
        self += self.pop == self.pop
    
    @property
    def lesser(self):
        self += self.pop < self.pop
    
    @property
    def greater(self):
        self += self.pop > self.pop
    
    @property
    def lesserequal(self):
        self += self.pop <= self.pop
    
    @property
    def greaterequal(self):
        self += self.pop >= self.pop
    
    @property
    def notequal(self):
        self += self.pop != self.pop
    
    @property
    def not_(self):
        self += not self.pop
    
    @property
    def neg(self):
        self += -self.pop
    
    #Object Operators
    def __iadd__(self, other):
        if other != self:
            self.append(other)
        return self
    
    def __lshift__(self, other):
        if isinstance(other, Stack):
            self += other.pop
        else:
            self += other
        return self
    
    def __rshift__(self, other):
        if isinstance(other, Stack):
            other += self.pop
        else:
            return NotImplemented
        return self
