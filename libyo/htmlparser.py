"""
----------------------------------------------------------------------
- htmlparser: Simple HTML Parser Implementation
----------------------------------------------------------------------
- Copyright (C) 2011-2013  Orochimarufan
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

import logging
import re

from collections import deque

from .compat.uni import unichr
from .compat.html import entities, parser

from .urllib.request import urlopen

from . import etree

logger = logging.getLogger(__name__)


class Document(object):
    """
    A DOM Document
    """
    def __init__(self, root):
        self.root = root
    
    def getroot(self):
        return self.root

    def get_element_by_id(self, id, default=None):
        return self.root.get_element_by_id(id)

    def find_class(self, name):
        return self.root.find_class(name)
    
    def find(self, path):
        return self.root.find(path)
    
    def findall(self, path):
        return self.root.findall(path)
    
    def iterfind(self, path):
        return self.root.iterfind(path)
    
    def findtext(self, path, default=None):
        return self.root.findtext(path, default)
    
    def iter(self):
        return self.root.iter()


class Mixin(object):
    # lxml.html api
    def drop_tree(self):
        """
        Drops the element and all its children.
        Unlike el.getparent().remove(el) this does not remove the tail text;
        with drop_tree the tail text is merged with the previous element.
        """
        prev = self.getprevious()
        if prev.tail is not None:
            prev.tail += self.tail
        else:
            prev.tail = self.tail
        self.getparent().remove(self)

    def drop_tag(self):
        """
        Remove the tag, but not its children or text. The children and text are merged into the parent.

        Example:

        >>> h = fragment_fromstring('<div>Hello <b>World!</b></div>')
        >>> h.find('.//b').drop_tag()
        >>> print(tostring(h, encoding=unicode))
        <div>Hello World!</div>
        """
        ix = self._index
        parent = self.getparent()
        if ix == 0:
            if parent.text is not None:
                parent.text += self.text + self.tail
            else:
                parent.text = self.text + self.tail
        else:
            elem = self.getprevious()
            if elem.tail is not None:
                elem.tail += self.text + self.tail
            else:
                elem.tail = self.text + self.tail
        for child in reversed(self._children):
            parent.insert(ix, child)
        parent.remove(self)

    def find_class(self, name):
        """
        Returns a list of all the elements with the given CSS class name.
        Note that class names are space separated in HTML, so doc.find_class_name('highlight')
        will find an element like <div class="sidebar highlight">. Class names are case sensitive.
        """
        return [elem for elem in self.iter() if name in elem.get("class", "").split(" ")]

    # TODO
    # def find_rel_links(self, rel):

    def get_element_by_id(self, id, default=None):
        """
        Return the element with the given id, or the default if none is found.
        If there are multiple elements with the same id (which there shouldn't be, but there often is),
        this returns only the first.
        """
        for elem in self.iter():
            if elem.get("id", None) == id:
                return elem

    def _iter_text_content(self):
        if self.text is not None:
            yield self.text
        stack = deque()
        node = self
        index = 0
        while True:
            if len(node) > index:
                index += 1
                node = node[index]
                stack.append(index)
                if node.text is not None:
                    yield node.text
                index = 0
            else:
                if not stack:
                    return
                if node.tail is not None:
                    yield node.tail
                index = stack.pop()
                node = node.getparent()

    def text_content(self):
        """
        Returns the text content of the element, including the text content of its children, with no markup.
        """
        return "".join(self._iter_text_content())


class Element(etree.Element, Mixin):
    # String representations
    def __repr__(self):
        """
        A readable representation
        """
        return "".join((
            "<%s Element" % self.tag,
            " id=%s" % self._attrib["id"] if "id" in self._attrib else "",
            " class=%s" % [i for i in self._attrib["class"].split(" ") if i] if "class" in self._attrib else "",
            " at 0x%x>" % id(self)))


class Comment(etree.Comment, Mixin):
    pass


class ProcessingInstruction(etree.ProcessingInstruction, Mixin):
    pass


class Parser(deque):
    """
    The Parser itself.
    """
    def __init__(self):
        super(Parser, self).__init__()
        self.root = None
    
    def open(self, name, attrs):
        """ Open a new Tag """
        if not len(self):
            if self.root is not None:
                raise ValueError("There can only be one root tag.")
            else:
                self.root = Element(name, attrs)
                self.append(self.root)
        else:
            this = Element(name, attrs)
            self[-1].append(this)
            self.append(this)
    
    def text(self, text):
        """ put Text data """
        if len(self) == 0:
            if not text.strip():
                return
            raise ValueError("Encountered text outside top-level element.")
        e = self[-1]
        if len(e):
            e = e[-1]
            if e.tail is not None:
                e.tail += text
            else:
                e.tail = text
        elif e.text is not None:
            e.text += text
        else:
            e.text = text
    
    def close(self, name):
        """
        Close a tag.
        and try to clean up messy html.
        """
        # try to get <p><img src='devil'></p> right
        # TODO: improve self-closing handling
        while len(self) > 2 and self[-1].tag != name and \
                self[-1].tag in ("input", "meta", "link", "br", "hr", "img", "button"):
            # move all children to the upper element
            self[-2].extend(self[-1])
            self.pop()
        
        # still no match?
        if self[-1].tag != name:
            # maybe the last tag was closed twice?
            for elem in self:
                if elem.tag == name:
                    # we found a matching open tag, so we'll assume that it was not
                    break
            else:
                # there are no matching open tags, so we'll assume it was
                logger.warn("Malformed HTML: %s closed twice (near: %s)" % (name, repr(self[-1])))
                return
            
            # pretend others were self-closing
            # XXX: just pop everything on malformed HTML?
            logger.warn("Malformed HTML: '%s' closed but last element on stack is %s" % (name, repr(self[-1])))
            while len(self) > 1 and self[-1].tag != name:
                self.pop()
        
        # pop the tag
        return self.pop()
    
    def comment(self, data):
        """ XML Comment """
        if len(self) == 0:
            raise ValueError("Encountered Comment outside root")
        self[-1].append(Comment(data))

    def pi(self, data):
        """ XML Processing Instruction """
        if len(self) == 0:
            raise ValueError("Encountered Processing Instruction outside root")
        self[-1].append(ProcessingInstruction(data))


class HTMLParser(parser.HTMLParser):
    """
    The stdlib-HTMLParser interface
    """
    def __init__(self, strict=False):
        self.parser = Parser()
        self.rawddata = ""
        super(HTMLParser, self).__init__(strict)
    
    def handle_starttag(self, name, attrs):
        self.parser.open(name, attrs)
    
    def handle_endtag(self, name):
        self.parser.close(name)
    
    def handle_data(self, data):
        self.parser.text(data)
    
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
        self.parser.comment(data)
    
    def handle_pi(self, data):
        if data.endswith("?") and data.lower().startswith("xml"):
            # "An XHTML processing instruction using the trailing '?'
            # will cause the '?' to be included in data." - HTMLParser
            # docs.
            #
            # Strip the question mark so we don't end up with two
            # question marks.
            data = data[:-1]
        self.parser.pi(data)

    def get_document(self):
        return Document(self.parser.root)

    def get_root(self):
        return self.parser.root


#simple url regex
_url_reg = re.compile(r'\w+://')

def parse(file_or_url):
    """
    Parses the named file or url, or if the object has a .read() method, parses from that.
    """
    p = HTMLParser()
    if hasattr(file_or_url, "read"):
        s = file_or_url.read()
        if isinstance(s, bytes):
            try:
                p.feed(s.decode("UTF-8"))
            except UnicodeDecodeError:
                p.feed(s.decode("Latin-1"))
        else:
            p.feed(s)
    elif _url_reg.match(file_or_url):
        with urlopen(file_or_url) as fp:
            try:
                p.feed(fp.read().decode("UTF-8"))
            except UnicodeDecodeError:
                p.feed(fp.read().decode("Latin-1"))
    else:
        with open(file_or_url, "r") as fp:
            p.feed(fp.read())
    return p.get_document()


def fragment_fromstring(markup, create_parent=None):
    """
    Returns an HTML fragment from a string. The fragment must contain just a single element, unless create_parent is given; e.g,. fragment_fromstring(string, create_parent='div') will wrap the element in a <div>.
    """
    p = HTMLParser()
    if create_parent is not None:
        p.parser.root = Element(create_parent, {})
        p.parser.append(p.parser.root)
    p.feed(markup)
    return p.get_root()

