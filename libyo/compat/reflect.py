
from __future__ import absolute_import,unicode_literals

from . import PY3

if PY3:
    def func_code(func):
        return func.__code__
    def func_defaults(func):
        return func.__defaults__
    def func_globals(func):
        return func.__globals__
    def im_func(im):
        return meth.__func__
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

__all__ = ["func_code","func_defaults","func_globals","im_func","im_self"]