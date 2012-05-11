"""
@author Orochimarufan
@module libyo.reflect.property
@created 2012-05-11
@modified 2012-05-11
"""

from __future__ import absolute_import, unicode_literals, division

property = property

class classproperty(property):
    def __get__(self,inst,klass):
        if klass is None:
            klass = type(inst)
        if isinstance(self.fget,classmethod):
            return self.fget.__get__(inst,klass)()
        return self.fget(klass)
    