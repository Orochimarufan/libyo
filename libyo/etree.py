"""
----------------------------------------------------------------------
- etree: Simple ElementTree Implementation
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

import re

from collections import deque

try:
    from xml.etree import ElementPath
except ImportError:
    try:
        from elementtree import ElementPath
    except ImportError:
        ElementPath = None

from . import tree


class ElementTree(object):
    """
    A DOM Tree
    """
    __slots__ = ("_root",)

    # TODO:
    # make methods on this respect the root

    def __init__(self, root):
        self._root = root

    def getroot(self):
        return self._root

    def _setroot(self, root):
        """
        Relocate the ElementTree to a new root node.
        """
        self._root = root

    def find(self, path, namespaces=None):
        """
        Finds the first toplevel element with given tag. Same as tree.getroot().find(path).
        """
        return self._root.find(path, namespaces)

    def findall(self, path, namespaces=None):
        """
        Finds all elements matching the ElementPath expression. Same as getroot().findall(path).
        """
        return self._root.findall(path, namespaces)

    def findtext(self, path, default=None, namespaces=None):
        """
        Finds the text for the first element matching the ElementPath expression. Same as getroot().findtext(path)
        """
        return self._root.findtext(path, default, namespaces)

    def getpath(self, element):
        """
        Returns a structural, absolute XPath expression to find that element.
        """
        raise NotImplementedError()

    def iter(self, *tags):
        """
        Creates an iterator for the root element. The iterator loops over all elements in this tree, in document order.
        """
        return self._root.iter(*tags)

    def iterfind(self, path, namespaces=None):
        """
        Iterates over all elements matching the ElementPath expression. Same as getroot().iterfind(path).
        """
        return self._root.iterfind(path, namespaces)

    def parse(self):
        """
        Updates self with the content of source and returns its root
        """
        raise NotImplementedError()

    def relaxng(self, relaxng):
        """
        Validate this document using other document.
        """
        raise NotImplementedError()

    def write(self, file, encoding=None, method="xml", pretty_print=False,
                xml_declaration=None, with_tail=True, standalone=None,
                compression=0, exclusive=False, with_comments=True,
                inclusive_ns_prefixes=None):
        """
        Write the tree to a filename, file or file-like object.
        """
        raise NotImplementedError()

    def write_c14n(self, file, exclusive=False, with_comments=True, compression=0, inclusive_ns_prefixes=None):
        """
        C14N write of document. Always writes UTF-8.
        """
        raise NotImplementedError()

    def xinclude(self):
        """
        Process the XInclude nodes in this document and include the referenced XML fragments.
        """
        raise NotImplementedError()

    def xmlschema(self, xmlschema):
        """
        Validate this document using other document.
        """
        raise NotImplementedError()

    def xpath(self, path, namespaces=None, extensions=None, smart_strings=True, **_variables):
        """
        XPath evaluate in context of document.
        """
        raise NotImplementedError()

    def xslt(self, xslt):
        """
        Transform this document using other document.
        """
        raise NotImplementedError()


class Element(tree.Element):
    """
    A DOM Element
    """
    __slots__ = ("_tag", "_attrib", "text", "tail")

    # Constructor
    def __init__(self, tag, attrib=None, **extra):
        """
        Create an Element.
        """
        super(Element, self).__init__()
        self._tag = tag
        if attrib is not None:
            self._attrib = dict(attrib)
        else:
            self._attrib = dict()
        if extra:
            self._attrib.update(extra)
        self.text = None
        self.tail = None

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

    # String representations
    def __repr__(self):
        """
        A readable representation
        """
        return "<%s Element at 0x%x>" % (self.tag, id(self))

    # lxml.etree api
    def clear(self):
        """
        Resets an element. This function removes all subelements, clears all attributes and sets the text and tail properties to None.
        """
        self._attrib = dict()
        self._text = None
        self._tail = None
        self._children = list()

    def makeelement(self, tag, attrib=None, **extra):
        """
        Create a new element with the same type.
        """
        return self.__class__(tag, attrib, **extra)

    # we use xml.etree's ElementPath implementation!
    if ElementPath is not None:
        class _SelectorContext(ElementPath._SelectorContext):
            # in this Tree implementation, every element knows his parent.
            class ParentMap:
                def __getitem__(self, elem):
                    return elem.getparent()
            parent_map = ParentMap()

        def iterfind(self, path, namespaces=None):
            # compile selector pattern
            if path[-1:] == "/":
                path = path + "*" # implicit all (FIXME: keep this?)
            try:
                selector = ElementPath._cache[path]
            except KeyError:
                if len(ElementPath._cache) > 100:
                    ElementPath._cache.clear()
                if path[:1] == "/":
                    raise SyntaxError("cannot use absolute path on element")
                it = iter(ElementPath.xpath_tokenizer(path, namespaces))
                next_ = lambda: next(it)
                token = next_()
                selector = []
                while 1:
                    try:
                        selector.append(ElementPath.ops[token[0]](next_, token))
                    except StopIteration:
                        raise SyntaxError("invalid path")
                    try:
                        token = next_()
                        if token[0] == "/":
                            token = next_()
                    except StopIteration:
                        break
                ElementPath._cache[path] = selector
            # execute selector pattern
            result = [self]
            context = self._SelectorContext(self)
            for select in selector:
                result = select(context, result)
            return result

        def find(self, path, namespaces=None):
            try:
                return next(self.iterfind(path, namespaces))
            except StopIteration:
                return None

        def findall(self, path, namespaces=None):
            return list(self.iterfind(path, namespaces))

        def findtext(self, path, default=None, namespaces=None):
            try:
                elem = next(self.iterfind(path, namespaces))
                return elem.text or ""
            except StopIteration:
                return default
    else:
        def iterfind(self, path, namespaces=None):
            raise ImportError("*find* functionality relies on xml.etree.ElementPath!")
        find = findall = iterfind
        def findtext(self, path, default=None, namespaces=None):
            raise ImportError("*find* functionality relies on xml.etree.ElementPath!")

    def get(self, attrib, default=None):
        """
        Gets an element attribute.
        """
        return self._attrib.get(attrib, default)

    def getroottree(self):
        """
        Return an ElementTree for the root node of the document that contains this element.

        This is the same as following element.getparent() up the tree until it returns None (for the root element) and then build an ElementTree for the last parent that was returned.
        """
        return ElementTree(self.getroot())

    def items(self):
        """
        Gets element attributes, as a sequence. The attributes are returned in an arbitrary order.
        """
        return self._attrib.items()

    def itertext(self, tag=None, with_tail=True, *tags):
        """
        Iterates over the text content of a subtree.
        """
        raise NotImplementedError()

    def keys(self):
        """
        Gets a list of attribute names. The names are returned in an arbitrary order (just like for an ordinary Python dictionary).
        """
        return self._attrib.keys()

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

    def xpath(self, path, namespaces=None, extensions=None, smart_strings=True, **_variables):
        """
        Evaluate an xpath expression using the element as context node.
        """
        raise NotImplementedError()


class _ContentOnlyElement(Element):
    __slots__ = ()

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
    __slots__ = ()

    @property
    def tag(self):
        return Comment

    def __repr__(self):
        return "<!--%s-->" % self.text


class ProcessingInstruction(_ContentOnlyElement):
    __slots__ = ()

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


def SubElement(parent, tag, attrib=None, **extra):
    """Subelement factory which creates an element instance, and appends it
    to an existing parent.

    The element tag, attribute names, and attribute values can be either
    bytes or Unicode strings.

    *parent* is the parent element, *tag* is the subelements name, *attrib* is
    an optional directory containing element attributes, *extra* are
    additional attributes given as keyword arguments.
    """
    e = parent.makeelement(tag, attrib, **extra)
    parent.append(e)
    return e

