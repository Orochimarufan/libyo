"""
----------------------------------------------------------------------
- compat.reflect: Reflection Compatibility module
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

from . import PY3

if PY3:
    def func_code(func):
        return func.__code__
    
    def func_defaults(func):
        return func.__defaults__
    
    def func_globals(func):
        return func.__globals__
    
    def im_func(im):
        return im.__func__
    
    def im_self(im):
        return im.__self__
else:
    def func_code(func):
        return func.func_code
    
    def func_defaults(func):
        return func.func_defaults
    
    def func_globals(func):
        return func.func_globals
    
    def im_func(im):
        return im.im_func
    
    def im_self(im):
        return im.im_self

__all__ = ["func_code", "func_defaults", "func_globals", "im_func", "im_self"]
