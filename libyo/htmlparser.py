"""
----------------------------------------------------------------------
- htmlparser: Simple HTML Parser Implementation
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

from __future__ import absolute_import, unicode_literals, division

from .compat import PY3
from .compat.uni import unichr

from collections import deque

from .compat.html import entities, parser


class Document(object):
    def __init__(self, root):
        self.root = root
    
    def getroot(self):
        return self.root


class DTag(object):
    def __init__(self, parent, name, data):
        self.parent = parent
        self.name = name
        self.text = data
        if parent:
            self.parent.children.append(self)
    
    def text_content(self):
        return self.text
    
    def __repr__(self):
        return "<{0} Data>".format(self.name)
    
    def get_element_by_id(self, id): #@ReservedAssignment
        return None
    
    def find_class(self, name, has=None):
        if has is None:
            has = []
        return has


class Tag(object):
    def __init__(self, parent, name, attrs):
        self.parent = parent
        self.name = name
        self.attrs = dict(attrs)
        self.children = []
        self.text = ""
        if parent:
            self.parent.children.append(self)
    
    def __getitem__(self, num):
        return self.children.__getitem__(num)
    
    def get_element_by_id(self, id): #@ReservedAssignment
        if "id" in self.attrs and self.attrs["id"] == id:
            return self
        for child in self.children:
            r = child.get_element_by_id(id)
            if r:
                return r
        else:
            return None
    
    def find_class(self, name, has=None):
        if has is None:
            has = []
        if "class" in self.attrs and name in self.attrs["class"].split(" "):
            has.append(self)
        for child in self.children:
            has = child.find_class(name, has)
        return has
    
    def get(self, name, default=None):
        return self.attrs.get(name, default)
    
    def text_content(self):
        return self.text
    
    def __repr__(self):
        return "<{0} Tag>".format(self.name)


class ParserStack(deque):
    def last(self):
        return self[-1]
    
    def open(self, name, attrs):
        if len(self) == 0:
            try:
                self.document
            except AttributeError:
                t = Tag(None, name, attrs)
                self.document = Document(t)
                t.parent = self.document
                self.append(t)
            else:
                raise ValueError("Only one top-level Tag allowed!")
        else:
            self.append(Tag(self.last(), name, attrs))
    
    def text(self, text):
        if len(self) == 0:
            return
        self.last().text += text
    
    def close(self):
        return self.pop()
    
    def data(self, name, data):
        if len(self) == 0:
            return #drop data before first tag
        DTag(self.last(), name, data)


class Parser(parser.HTMLParser):
    def __init__(self, *a, **b):
        self.stack = ParserStack()
        self.rawddata = ""
        if PY3:
            super(Parser, self).__init__(*a, **b)
        else:
            parser.HTMLParser.__init__(self, *a, **b)
    
    def handle_starttag(self, name, attrs):
        self.stack.open(name, attrs)
    
    def handle_endtag(self, name):
        self.stack.close()
    
    def handle_data(self, data):
        self.stack.text(data)
    
    def handle_charref(self, name):
        if name.startswith("x"):
            i = int(name.lstrip("x"), 16)
        else:
            i = int(name)
        try:
            c = unichr(i)
        except (ValueError, OverflowError):
            c = ""
        self.handle_data(c)
    
    def handle_entityref(self, name):
        i = entities.name2codepoint.get(name)
        if i is not None:
            c = unichr(i)
        else:
            c = "&{0};".format(name)
        self.handle_data(c)
    
    def handle_comment(self, data):
        self.stack.data("comment", data)
    
    def handle_pi(self, data):
        if data.endswith("?") and data.lower().startswith("xml"):
            # "An XHTML processing instruction using the trailing '?'
            # will cause the '?' to be included in data." - HTMLParser
            # docs.
            #
            # Strip the question mark so we don't end up with two
            # question marks.
            data = data[:-1]
        self.stack.data("ProcessingInstruction", data)


def parse(markup):
    p = Parser()
    if hasattr(markup, "read"):
        markup = markup.read()
    if type(markup) is bytes:
        markup = markup.decode("UTF-8")
    p.feed(markup)
    return p.stack.document


def fragment_fromstring(markup):
    p = Parser()
    p.feed(markup)
    return p.stack.document.root
