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

import logging
import re

from collections import deque

from .compat import PY3
from .compat.uni import unichr
from .compat.html import entities, parser

from .urllib.request import urlopen

if PY3:
    import builtins
else:
    import __builtin__ as builtins

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


class Element(object):
    """
    A DOM Element
    """
    __slots__ = ("_parent","_tag","_attrib","text","tail","_children")

    # Properties
    @property
    def tag(self):
        """
        Element tag
        """
        return self._tag

    @property
    def attrib(self):
        """
        Element attribute dictionary. Where possible, use get(), set(), keys(), values() and items() to access element attributes.
        """
        return dict(self._attrib)

    @property
    def _index(self):
        return self._parent.index(self)

    # Constructor
    def __init__(self, tag, attrib):
        """
        Create an Element.
        """
        self._parent = None
        self._tag = tag
        self._attrib = dict(attrib)
        self.text = None
        self.tail = None
        self._children = list()

    # String representations
    def __repr__(self):
        """
        A readable representation
        """
        return "".join((
            "<%s Element" % self.tag,
            " id=%s" % self._attrib["id"] if "id" in self._attrib else "",
            " class=%s" % self._attrib["class"] if "class" in self._attrib else "",
            " at 0x%x>" % id(self)))

    # sequence api
    def __contains__(self, elem):
        return elem in self._children

    def __delitem__(self, index):
        del self._children[index]

    def __getitem__(self, index):
        return self._children[index]

    def __iter__(self):
        return iter(self._children)

    def __len__(self):
        return len(self._children)

    def __reversed__(self):
        return reversed(self._children)

    def __setitem__(self, index, elem):
        elem._assign(self)
        self._children[index] = elem

    def _assign(self, parent):
        if self._parent is not None:
            self._parent.remove(self)
        self._parent = parent

    # lxml.etree api
    def addnext(self, elem):
        """
        Adds the element as a following sibling directly after this element.

        This is normally used to set a processing instruction or comment after the root node of a document. Note that tail text is automatically discarded when adding at the root level.
        """
        self._parent.insert(self._index + 1, elem)

    def addprevious(self, elem):
        """
        Adds the element as a preceding sibling directly before this element.

        This is normally used to set a processing instruction or comment before the root node of a document. Note that tail text is automatically discarded when adding at the root level.
        """
        self._parent.insert(self._index, elem)

    def append(self, elem):
        """
        Adds a subelement to the end of this element.
        """
        elem._assign(self)
        self._children.append(elem)

    def clear(self):
        """
        Resets an element. This function removes all subelements, clears all attributes and sets the text and tail properties to None.
        """
        self._attrib = dict()
        self._text = None
        self._tail = None
        self._children = list()

    def extend(self, elements):
        """
        Extends the current children by the elements in the iterable.
        """
        for elem in elements:
            self.append(elem)

    # TODO
    # def find(path):
    # def findall(path):
    # def findtext(path):

    def get(self, attrib, default=None):
        """
        Gets an element attribute.
        """
        return self._attrib.get(attrib, default)

    def getnext(self):
        """
        Returns the following sibling of this element or None.
        """
        ix = self._index
        if ix == len(self._parent):
            return None
        return self._parent[ix + 1]

    def getparent(self):
        """
        Returns the parent of this element or None for the root element.
        """
        return self._parent

    def getprevious(self):
        """
        Returns the preceding sibling of this element or None.
        """
        ix = self._index
        if ix == 0:
            return None
        return self._parent[ix - 1]

    def getroottree(self):
        """
        Return an ElementTree for the root node of the document that contains this element.

        This is the same as following element.getparent() up the tree until it returns None (for the root element) and then build an ElementTree for the last parent that was returned.
        """
        parent = self
        while parent is not None:
            parent = parent.getparent()
        return Document(parent)

    def index(self, elem):
        """
        Find the position of the child within the parent.
        """
        return self._children.index(elem)

    def insert(self, index, element):
        """
        Inserts a subelement at the given position in this element
        """
        element._assign(self)
        self._children.insert(index, element)

    def items(self):
        """
        Gets element attributes, as a sequence. The attributes are returned in an arbitrary order.
        """
        return self._attrib.items()

    def iter(self, *tags):
        """
        Iterate over all elements in the subtree in document order (depth first pre-order), starting with this element.

        Can be restricted to find only elements with a specific tag.

        Passing a sequence of tags will let the iterator return all elements matching any of these tags, in document order.
        """
        stack = deque([self])
        if tags:
            while stack:
                node = stack.pop()
                if node.tag in tags:
                    yield node
                stack.extend(reversed(node))
        else:
            while stack:
                node = stack.popleft()
                yield node
                stack.extend(reversed(node))

    def iterancestors(self, *tags):
        """
        Iterate over the ancestors of this element (from parent to parent).
        """
        x = self._parent
        while x is not None:
            yield x
            x = x.getparent()

    def iterchildren(self, tag=None, reversed=False, *tags):
        """
        Iterate over the children of this element.

        As opposed to using normal iteration on this element, the returned elements can be reversed with the 'reversed' keyword and restricted to find only elements with a specific tag
        """
        if tags is None:
            tags = list()
        if tag is not None:
            tags.insert(0, tag)
        x = builtins.reversed(self._children) if reversed else iter(self._children)
        if tags:
            return (child for child in x if child.tag in tags)
        else:
            return x

    def iterdescendants(self, *tags):
        """
        Iterate over the descendants of this element in document order.

        As opposed to el.iter(), this iterator does not yield the element itself. The returned elements can be restricted to find only elements with a specific tag, see iter.
        """
        stack = deque(reversed(self._children))
        if tags:
            while stack:
                node = stack.pop()
                if node.tag in tags:
                    yield node
                stack.extend(reversed(node))
        else:
            while stack:
                node = stack.pop()
                yield node
                stack.extend(reversed(node))

    # TODO
    # def iterfind(self, path):

    def itersiblings(self, tag=None, preceding=False, *tags):
        """
        Iterate over the following or preceding siblings of this element.

        The direction is determined by the 'preceding' keyword which defaults to False, i.e. forward iteration over the following siblings. When True, the iterator yields the preceding siblings in reverse document order, i.e. starting right before the current element and going backwards.

        Can be restricted to find only elements with a specific tag
        """
        if tags is None:
            tags = list()
        if tag is not None:
            tags.insert(0, tag)
        x = reversed(self._parent[:self._index]) if preceding else iter(self._parent[self._index+1:])
        if tags:
            return (sib for sib in x if sib.tag in tags)
        else:
            return x
    # TODO
    # def itertext(self, tag=None, with_tail=True, *tags):

    def keys(self):
        """
        Gets a list of attribute names. The names are returned in an arbitrary order (just like for an ordinary Python dictionary).
        """
        return self._attrib.keys()

    def remove(self, elem):
        """
        Removes a matching subelement. Unlike the find methods, this method compares elements based on identity, not on tag value or contents.
        """
        self._children.remove(elem)

    def replace(self, elem, new_elem):
        """
        Replaces a subelement with the element passed as second argument.
        """
        new_elem._assign(self)
        self._children[self._children.index(elem)] = new_elem

    def set(self, attrib, value):
        """
        Sets an element attribute.
        """
        self._attrib[attrib] = value

    def values(self):
        """
        Gets element attribute values as a sequence of strings. The attributes are returned in an arbitrary order.
        """
        return self._attrib.values()

    # TODO
    # def xpath(self, path, ...):

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
        parent = self.getparent()
        if parent.text is not None:
            parent.text += self.text + self.tail
        else:
            parent.text = self.text + self.tail
        ix = self._index
        for child in reversed(self._children):
            parent.insert(ix, child)
        parent.remove(self)

    def find_class(self, name):
        """
        Returns a list of all the elements with the given CSS class name.
        Note that class names are space separated in HTML, so doc.find_class_name('highlight')
        will find an element like <div class="sidebar highlight">. Class names are case sensitive.
        """
        return [elem for elem in self.iter() if name in elem.get("class", [])]

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


class _ContentOnlyElement(Element):
    __slots__ = ("_parent","text","tail")

    def __init__(self, text=None):
        self._parent = None
        self.tail = None
        self.text = text

    def _raiseImmutable(self):
        raise TypeError("this element does not have children or attributes")

    def set(self, key, default=None):
        _raiseImmutable()

    def append(self, elem):
        _raiseImmutable()

    def insert(self, index, elem):
        _raiseImmutable()

    def __setitem__(self, index, elem):
        _raiseImmutable()

    def __reversed__(self):
        return []

    def __iter__(self):
        return iter([])

    def __delitem__(self, index):
        _raiseImmutable()

    def __contains__(self, other):
        return False

    @property
    def attrib(self):
        return {}

    def __getitem__(self, i):
        if isinstance(i, slice):
            return []
        else:
            raise IndexError("list index out of range")

    def get(self, value, default=None):
        return default

    keys = values = items = lambda self: []


class Comment(_ContentOnlyElement):
    @property
    def tag(self):
        return Comment

    def __repr__(self):
        return "<!--%s-->" % self.text


class ProcessingInstruction(_ContentOnlyElement):
    @property
    def tag(self):
        return ProcessingInstruction

    _FIND_PI_ATTRIBUTES = re.compile(r'\s+(\w+)\s*=\s*(?:\'([1\']*)\'|"([^"]*)")', re.U).findall

    @property
    def attrib(self):
        """
        Returns a dict containing all pseudo-attributes that can be
        parsed from the text content of this processing instruction.
        Note that modifying the dict currently has no effect on the
        XML node, although this is not guaranteed to stay this way.
        """
        return { attr : (value1 or value2)
               for attr, value1, value2 in self._FIND_PI_ATTRIBUTES(' ' + self.text) }

    def get(self, key, default=None):
        """
        Try to parse pseudo-attributes from the text content of the
        processing instruction, search for one with the given key as
        name and return its associated value.

        Note that this is only a convenience method for the most
        common case that all text content is structured in
        attribute-like name-value pairs with properly quoted values.
        It is not guaranteed to work for all possible text content.
        """
        return self.attrib.get(key, default)


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


def fragment_fromstring(markup):
    p = HTMLParser()
    p.feed(markup)
    return p.get_root()

