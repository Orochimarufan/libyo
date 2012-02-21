#
#       configparser.py
#       
#       Copyright 2011 Hinata-chan <orochimarufan.x3@gmail.com>
#       
#       Redistribution and use in source and binary forms, with or without
#       modification, are permitted provided that the following conditions are
#       met:
#       
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#       * Redistributions in binary form must reproduce the above
#         copyright notice, this list of conditions and the following disclaimer
#         in the documentation and/or other materials provided with the
#         distribution.
#       * Neither the name of the  nor the names of its
#         contributors may be used to endorse or promote products derived from
#         this software without specific prior written permission.
#       
#       THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#       "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#       LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#       A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#       OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#       SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#       LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#       DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#       THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#       (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#       OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""
libyo.configparser (MyConfigParser)
(c) 2011 by Orochimarufan

An Addition to the configparser module

Adds RawSpecialConfigParser class.
Adds SpecialConfigParser class.
Adds RawPcsxConfigParser class.
Adds PcsxConfigParser class.
[not recommended]:
Adds UConfigParser class.
Adds UInterpolation class.
Adds UPathError class.

RawPcsxConfigParser Provides a RawConfigParser supporting non-sectioned values.
PcsxConfigParser Provides a RawPcsxConfigParser with Interpolation features.
RawSpecialConfigParser Adds a list feature to RawPcsxConfigParser
SpecialConfigParser Provides Interpolation Features for RawSpecialConfigParser

UConfigParser Provides a simple filesystem-like structure in INI-Files.
UInterpolation Provides a simple filesystem-like Interpolation Notation (${section/option})"""

import sys
PY_MAJOR_VERSION=sys.version_info[0]
if PY_MAJOR_VERSION==3:
    from configparser import ConfigParser, RawConfigParser, SectionProxy
    from configparser import BasicInterpolation, ExtendedInterpolation as CPEI, Interpolation
    from configparser import Error, DuplicateOptionError, DuplicateSectionError, MissingSectionHeaderError, NoOptionError, NoSectionError, ParsingError
    from configparser import InterpolationError, InterpolationDepthError, InterpolationMissingOptionError, InterpolationSyntaxError
    from configparser import DEFAULTSECT, MAX_INTERPOLATION_DEPTH, _UNSET
else:
    from .compat.python2.configparser import ConfigParser, RawConfigParser, SectionProxy
    from .compat.python2.configparser import BasicInterpolation, ExtendedInterpolation as CPEI, Interpolation
    from .compat.python2.configparser import Error, DuplicateOptionError, DuplicateSectionError, MissingSectionHeaderError, NoOptionError, NoSectionError, ParsingError
    from .compat.python2.configparser import InterpolationError, InterpolationDepthError, InterpolationMissingOptionError, InterpolationSyntaxError
    from .compat.python2.configparser import DEFAULTSECT, MAX_INTERPOLATION_DEPTH, _UNSET
import posixpath
import itertools

#+ ide fix to prevent unused imports warnings
__fix=( 
        Interpolation, BasicInterpolation,
        Error, MissingSectionHeaderError, ParsingError,
        InterpolationError, DEFAULTSECT, MAX_INTERPOLATION_DEPTH)
del __fix
#- ide fix

__all__ = ["NoSectionError", "DuplicateOptionError", "DuplicateSectionError",
           "NoOptionError", "InterpolationError", "InterpolationDepthError",
           "InterpolationSyntaxError", "ParsingError", "UPathError", 
           "MissingSectionHeaderError",
           "PcsxConfigParser","UConfigParser", "ConfigParser", "RawConfigParser",
           "RawPcsxConfigParser", "RawSpecialConfigParser", "SpecialConfigParser",
           "DEFAULTSECT", "MAX_INTERPOLATION_DEPTH"]
__export__ = ["NoSectionError", "DuplicateOptionError", "DuplicateSectionError",
           "NoOptionError", "InterpolationError", "InterpolationDepthError",
           "InterpolationSyntaxError", "ParsingError",
           "UPathError", "MissingSectionHeaderError",
           "UInterpolation", "BasicInterpolation",
           "ExtendedInterpolation", "Interpolation"
           "PcsxConfigParser", "UConfigParser", "ConfigParser", "RawConfigParser",
           "RawPcsxConfigParser", "RawSpecialConfigParser", "SpecialConfigParser",
           "DEFAULTSECT", "MAX_INTERPOLATION_DEPTH"]

#[PcsxConfigParser]
class RawPcsxConfigParser(RawConfigParser): #needed for configs having values out of the sections
    """Provides an Interface to Config files featuring non-sectioned data.
    RawPcsxConfigParser.NOSECT specifies where to put items not having any section defined
    RawPcsxConfigParser.NOSECT_COMMENT specifies wether or not (None) to put a comment before non-sectioned data and what"""
    NOSECT="__DEFAULT__" # Where to put items without a section?
    NOSECT_COMMENT="#[NO SECTION]; The following data is not provided without section information!"
    #NOSECT_COMMENT=None
    def getnosect(self,key,fallback=_UNSET):
        return self.get(self.NOSECT,key,fallback=fallback)
    def _read(self, fp, fpname):
        """Parse a sectioned configuration file.

        Each section in a configuration file contains a header, indicated by
        a name in square brackets (`[]'), plus key/value options, indicated by
        `name' and `value' delimited with a specific substring (`=' or `:' by
        default).

        Values can span multiple lines, as long as they are indented deeper
        than the first line of the value. Depending on the parser's mode, blank
        lines may be treated as parts of multiline values or ignored.

        Configuration files may include comments, prefixed by specific
        characters (`#' and `;' by default). Comments may appear on their own
        in an otherwise empty line or may be entered in lines holding values or
        section names.
        """
        elements_added = set()
        cursect = None                        # None, or a dictionary
        sectname = None
        optname = None
        lineno = 0
        indent_level = 0
        e = None                              # None, or an exception
        for lineno, line in enumerate(fp, start=1):
            comment_start = None
            # strip inline comments
            for prefix in self._inline_comment_prefixes:
                index = line.find(prefix)
                if index == 0 or (index > 0 and line[index-1].isspace()):
                    comment_start = index
                    break
            # strip full line comments
            for prefix in self._comment_prefixes:
                if line.strip().startswith(prefix):
                    comment_start = 0
                    break
            value = line[:comment_start].strip()
            if not value:
                if self._empty_lines_in_values:
                    # add empty line to the value, but only if there was no
                    # comment on the line
                    if (comment_start is None and
                        cursect is not None and
                        optname and
                        cursect[optname] is not None):
                        cursect[optname].append('') # newlines added at join
                else:
                    # empty line marks end of value
                    indent_level = sys.maxsize
                continue
            # continuation line?
            first_nonspace = self.NONSPACECRE.search(line)
            cur_indent_level = first_nonspace.start() if first_nonspace else 0
            if (cursect is not None and optname and
                cur_indent_level > indent_level):
                cursect[optname].append(value)
            # a section header or option header?
            else:
                indent_level = cur_indent_level
                # is it a section header?
                mo = self.SECTCRE.match(value)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        if self._strict and sectname in elements_added:
                            raise DuplicateSectionError(sectname, fpname,
                                                        lineno)
                        cursect = self._sections[sectname]
                        elements_added.add(sectname)
                    elif sectname == self.default_section:
                        cursect = self._defaults
                    else:
                        cursect = self._dict()
                        self._sections[sectname] = cursect
                        self._proxies[sectname] = SectionProxy(self, sectname)
                        elements_added.add(sectname)
                    # So sections can't start with a continuation line
                    optname = None
                # no section header in the file?
                #elif cursect is None:
                    #raise MissingSectionHeaderError(fpname, lineno, line)
                    #vvv handeled below vvv
                # an option line?
                else:
                    mo = self._optcre.match(value)
                    if mo:
                        if cursect is None and (self.NOSECT not in self._sections or self.NOSECT not in self._proxies):
                            sectname=self.NOSECT
                            cursect=self._dict()
                            self._sections[self.NOSECT]=cursect
                            self._proxies[self.NOSECT]=SectionProxy(self, self.NOSECT)
                            elements_added.add(self.NOSECT)
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        if not optname:
                            e = self._handle_error(e, fpname, lineno, line)
                        optname = self.optionxform(optname.rstrip())
                        if (self._strict and
                            (sectname, optname) in elements_added):
                            raise DuplicateOptionError(sectname, optname,
                                                       fpname, lineno)
                        elements_added.add((sectname, optname))
                        # This check is fine because the OPTCRE cannot
                        # match if it would set optval to None
                        if optval is not None:
                            optval = optval.strip()
                            cursect[optname] = [optval]
                        else:
                            # valueless option handling
                            cursect[optname] = None
                    else:
                        # a non-fatal parsing error occurred. set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        e = self._handle_error(e, fpname, lineno, line)
        # if any parsing errors occurred, raise an exception
        if e:
            raise e
        self._join_multiline_values()
    def write(self, fp, space_around_delimiters=True):
        """Write an .ini-format representation of the configuration state.

        If `space_around_delimiters' is True (the default), delimiters
        between keys and values are surrounded by spaces.
        """
        if space_around_delimiters:
            d = " {} ".format(self._delimiters[0])
        else:
            d = self._delimiters[0]
        if self.NOSECT in self._sections:
            self._write_nosect(fp, self._sections[self.NOSECT].items(), d)
        if self._defaults:
            self._write_section(fp, self.default_section,
                                    self._defaults.items(), d)
        for section in self._sections:
            if section==self.NOSECT:
                continue
            self._write_section(fp, section,
                                self._sections[section].items(), d)
    def _write_nosect(self, fp, section_items, delimiter):
        """Write the Values without a section"""
        if self.NOSECT_COMMENT is not None:
            fp.write(self.NOSECT_COMMENT+"\n")
        for key, value in section_items:
            value = self._interpolation.before_write(self, self.NOSECT, key, value)
            if value is not None or not self._allow_no_value:
                value = delimiter + str(value).replace("\n","\n\t")
            else:
                value = ""
            fp.write("{}{}\n".format(key, value))
        fp.write("\n")

class PcsxConfigParser(RawPcsxConfigParser, ConfigParser): pass
    #Apply Changes made in ConfigParser to RawPcsxConfigParser

class ExtendedInterpolation(CPEI):
    """FIX/libyo; use libyo.configparser.CPEI for original version"""
    def _interpolate_some(self, parser, option, accum, rest, section, map,
                          depth):
        if depth > MAX_INTERPOLATION_DEPTH:
            raise InterpolationDepthError(option, section, rest)
        while rest:
            p = rest.find("$")
            if p < 0:
                accum.append(rest)
                return
            if p > 0:
                accum.append(rest[:p])
                rest = rest[p:]
            # p is no longer used
            c = rest[1:2]
            if c == "$":
                accum.append("$")
                rest = rest[2:]
            elif c == "{":
                m = self._KEYCRE.match(rest)
                if m is None:
                    raise InterpolationSyntaxError(option, section,
                        "bad interpolation variable reference %r" % rest)
                path = m.group(1).split(':')
                rest = rest[m.end():]
                sect = section
                opt = option
                try:
                    if len(path) == 1:
                        opt = parser.optionxform(path[0])
                        v = map[opt]
                    elif len(path) == 2:
                        sect = path[0]
                        opt = parser.optionxform(path[1])
                        v = parser.get(sect, opt, raw=True)
                    else:
                        raise InterpolationSyntaxError(
                            option, section,
                            "More than one ':' found: %r" % (rest,))
                except (KeyError, NoSectionError, NoOptionError):
                    raise InterpolationMissingOptionError(
                        option, section, rest, ":".join(path))
                if "$" in v:
                    self._interpolate_some(parser, opt, accum, v, sect,
                                           dict(parser.items(sect, raw=True)),
                                           depth + 1)
                else:
                    accum.append(v)
            else:
                raise InterpolationSyntaxError(
                    option, section,
                    "'$' must be followed by '$' or '{', "
                    "found: %r" % (rest,))

#[SpecialConfigParser]
class RawSpecialConfigParser(RawPcsxConfigParser):
    """
    RawSpecialConfigParser
    
    Provides Support for NON-SECTIONED (like RawPcsxConfigParser) Options
    and List Values in INI-Formatted files.
    
    SYNTAX:
    (file begins)
    #no section defined
    option=value
    #now a list
    list[]=1
    list[]=2
    list[]=3
    (file ends)
    
    modify ParserObject.NOSECT to specify where Options without a section defined are stored.
    """
    def _read(self, fp, fpname):
        """Parse a sectioned configuration file.

        Each section in a configuration file contains a header, indicated by
        a name in square brackets (`[]'), plus key/value options, indicated by
        `name' and `value' delimited with a specific substring (`=' or `:' by
        default).

        Values can span multiple lines, as long as they are indented deeper
        than the first line of the value. Depending on the parser's mode, blank
        lines may be treated as parts of multiline values or ignored.

        Configuration files may include comments, prefixed by specific
        characters (`#' and `;' by default). Comments may appear on their own
        in an otherwise empty line or may be entered in lines holding values or
        section names.
        """
        elements_added = set()
        cursect = None                        # None, or a dictionary
        sectname = None
        optname = None
        lineno = 0
        indent_level = 0
        list_index = 0
        list_list = set()
        e = None                              # None, or an exception
        for lineno, line in enumerate(fp, start=1):
            comment_start = None
            # strip inline comments
            for prefix in self._inline_comment_prefixes:
                index = line.find(prefix)
                if index == 0 or (index > 0 and line[index-1].isspace()):
                    comment_start = index
                    break
            # strip full line comments
            for prefix in self._comment_prefixes:
                if line.strip().startswith(prefix):
                    comment_start = 0
                    break
            value = line[:comment_start].strip()
            if not value:
                if self._empty_lines_in_values:
                    # add empty line to the value, but only if there was no
                    # comment on the line
                    if (comment_start is None and
                        cursect is not None and
                        optname and
                        cursect[optname] is not None):
                        cursect[optname].append('') # newlines added at join
                else:
                    # empty line marks end of value
                    indent_level = sys.maxsize
                continue
            # continuation line?
            first_nonspace = self.NONSPACECRE.search(line)
            cur_indent_level = first_nonspace.start() if first_nonspace else 0
            if (cursect is not None and optname and cur_indent_level > indent_level):
                if (sectname,optname) in list_list:
                    cursect[optname][list_index].append(value)
                else:
                    cursect[optname].append(value)
            # a section header or option header?
            else:
                indent_level = cur_indent_level
                # is it a section header?
                mo = self.SECTCRE.match(value)
                if mo:
                    sectname = mo.group('header')
                    if sectname in self._sections:
                        if self._strict and sectname in elements_added:
                            raise DuplicateSectionError(sectname, fpname,
                                                        lineno)
                        cursect = self._sections[sectname]
                        elements_added.add(sectname)
                    elif sectname == self.default_section:
                        cursect = self._defaults
                    else:
                        cursect = self._dict()
                        self._sections[sectname] = cursect
                        self._proxies[sectname] = SectionProxy(self, sectname)
                        elements_added.add(sectname)
                    # So sections can't start with a continuation line
                    optname = None
                # no section header in the file?
                #elif cursect is None:
                    #raise MissingSectionHeaderError(fpname, lineno, line)
                    #vvv handeled below vvv
                # an option line?
                else:
                    mo = self._optcre.match(value)
                    if mo:
                        if cursect is None and (self.NOSECT not in self._sections or self.NOSECT not in self._proxies):
                            sectname=self.NOSECT
                            cursect=self._dict()
                            self._sections[self.NOSECT]=cursect
                            self._proxies[self.NOSECT]=SectionProxy(self, self.NOSECT)
                            elements_added.add(self.NOSECT)
                        optname, vi, optval = mo.group('option', 'vi', 'value')
                        if not optname:
                            e = self._handle_error(e, fpname, lineno, line)
                        optname = self.optionxform(optname.rstrip())
                        if optname[-2:]=="[]":
                            optname=optname[:-2]
                            if (sectname, optname) not in elements_added:
                                cursect[optname]=[]
                                elements_added.add((sectname, optname))
                                list_list.add((sectname, optname))
                            if optval is not None:
                                optval = optval.strip()
                                cursect[optname].append([optval])
                            else:
                                cursect[optname].append(None)
                            list_index=len(cursect[optname])-1
                        else:
                            if (self._strict and
                                (sectname, optname) in elements_added):
                                raise DuplicateOptionError(sectname, optname,
                                                           fpname, lineno)
                            elements_added.add((sectname, optname))
                            # This check is fine because the OPTCRE cannot
                            # match if it would set optval to None
                            if optval is not None:
                                optval = optval.strip()
                                cursect[optname] = [optval]
                            else:
                                # valueless option handling
                                cursect[optname] = None
                    else:
                        # a non-fatal parsing error occurred. set up the
                        # exception but keep going. the exception will be
                        # raised at the end of the file and will contain a
                        # list of all bogus lines
                        e = self._handle_error(e, fpname, lineno, line)
        # if any parsing errors occurred, raise an exception
        self.__lists = list_list
        if e:
            raise e
        self._join_multiline_values()
    def _join_multiline_values(self):
        defaults = self.default_section, self._defaults
        all_sections = itertools.chain((defaults,), self._sections.items())
        for section, options in all_sections:
            for name, val in options.items():
                if (section,name) in self.__lists:
                    options[name] = [ self.__join_mlv(section,name,i) for i in val ]
                    # dirty hack to avoid x[]= entries
                    options[name] = [ i for i in options[name] if i != "" ]
                else:
                    options[name] = self.__join_mlv(section,name,val)
    def __join_mlv(self,section, name, val):
        if isinstance(val, list):
            val = '\n'.join(val).rstrip()
        return self._interpolation.before_read(self, section, name, val)
    def _write_section(self, fp, section_name, section_items, delimiter):
        """Write a single section to the specified `fp'."""
        fp.write("[{}]\n".format(section_name))
        for key, value in section_items:
            if value.__class__.__name__=="list":
                for i in value:
                    self._write_option(fp, delimiter, section_name, key+"[]", i)
            else:
                self._write_option(fp, delimiter, section_name, key, value)
        fp.write("\n")
    def _write_nosect(self, fp, section_items, delimiter):
        """Write the Values without a section"""
        if self.NOSECT_COMMENT is not None:
            fp.write(self.NOSECT_COMMENT+"\n")
        for key, value in section_items:
            if value.__class__.__name__=="list":
                for i in value:
                    self._write_option(fp, delimiter, self.NOSECT, key+"[]", i)
            else:
                self._write_option(fp, delimiter, self.NOSECT, key, value)
        fp.write("\n")
    def _write_option(self,fp,delimiter,section,key,value):
        value = self._interpolation.before_write(self, section, key, value)
        if value is not None or not self._allow_no_value:
            value = delimiter + str(value).replace("\n","\n\t")
        else:
            value = ""
        fp.write("{}{}\n".format(key, value))
    def _validate_value_types(self, section="", option="", value=""):
        """Raises a TypeError for non-string values.

        The only legal non-string value if we allow valueless
        options is None, so we need to check if the value is a
        string if:
        - we do not allow valueless options, or
        - we allow valueless options but the value is not None

        For compatibility reasons this method is not used in classic set()
        for RawConfigParsers. It is invoked in every case for mapping protocol
        access and in ConfigParser.set().
        
        SpecialConfigParser also allows Lists of Strings
        """
        if not isinstance(section, str):
            raise TypeError("section names must be strings")
        if not isinstance(option, str):
            raise TypeError("option keys must be strings")
        if not self._allow_no_value or value:
            try:
                [isinstance(i,str) for i in value].index(False)
            except:
                pass
            else:
                raise TypeError("option values must be strings or lists of strings")
    def set(self,section,option,value):
        if isinstance(value,list):
            value = [self._interpolation.before_set(self, section, option, i) for i in value]
        elif value:
            value = self._interpolation.before_set(self, section, option, value)
        if not section or section == self.default_section:
            sectdict = self._defaults
        else:
            try:
                sectdict = self._sections[section]
            except KeyError:
                raise NoSectionError(section)
        sectdict[self.optionxform(option)] = value
    def get(self, section, option, raw=False, vars=None, fallback=_UNSET):
        try:
            d = self._unify_values(section, vars)
        except NoSectionError:
            if fallback is _UNSET:
                raise
            else:
                return fallback
        option = self.optionxform(option)
        try:
            value = d[option]
        except KeyError:
            if fallback is _UNSET:
                raise NoOptionError(option, section)
            else:
                return fallback

        if raw or value is None:
            return value
        elif isinstance(value,list):
            return [self._interpolation.before_get(self, section, option, i, d) for i in value]
        else:
            return self._interpolation.before_get(self, section, option, value, d)

class SpecialConfigParser(ConfigParser,RawSpecialConfigParser):
    """
    SpecialConfigParser
    
    Provides Support for NON-SECTIONED (like PcsxConfigParser) Options
    and List Values in INI-Formatted files.
    
    SYNTAX:
    (file begins)
    #no section defined
    option=value
    #now a list
    list[]=1
    list[]=2
    list[]=3
    (file ends)
    
    Modify ParserObject.NOSECT to specify where Options without a section defined are stored.
    Use RawSpecialConfigParser if you do not need to support Interpolation.
    """
    pass

#[UConfigParser] and [UInterpolation] Stuff
class UPathError(Error): pass

class UInterpolation(ExtendedInterpolation):
    """UInterpolation [class(ExtendedInterpolation)]
    replaces:
        _interpolate_some()
            @ARG parser
            @ARG option
            @ARG accum
            @ARG rest
            @ARG section
            @ARG map
            @ARG depth
            @DSC Interpolates over One Interpolation and loops
            @SYN ${section/option} ${name} DELIM=last(/)"""
    def _interpolate_some(self, parser, option, accum, rest, section, omap, depth):
        """@ARG parser
        @ARG option
        @ARG accum
        @ARG rest
        @ARG section
        @ARG omap
        @ARG depth
        @DSC Interpolates over One Interpolation and loops
        @SYN ${/path/name} ${name} DELIM=last(/)"""
        if depth > MAX_INTERPOLATION_DEPTH:
            raise InterpolationDepthError(option, section, rest)
        while rest:
            p = rest.find("$")
            if p < 0:
                accum.append(rest)
                return
            if p > 0:
                accum.append(rest[:p])
                rest = rest[p:]
            # p is no longer used
            c = rest[1:2]
            if c == "$":
                accum.append("$")
                rest = rest[2:]
            elif c == "{":
                m = self._KEYCRE.match(rest)
                if m is None:
                    raise InterpolationSyntaxError(option, section,
                        "bad interpolation variable reference %r" % rest)
                path = list(posixpath.split(parser.optionxform(m.group(1))))
                if path[0]=="":
                    path.pop(0)
                rest = rest[m.end():]
                sect = section
                opt = option
                try:
                    if len(path) == 1:
                        opt = path[0]
                        v = omap[opt]
                    elif len(path) == 2:
                        sect = path[0]
                        opt = path[1]
                        v = parser.get(sect, opt, raw=True)
                    else:
                        raise InterpolationSyntaxError(
                            option, section,
                            "More than one ':' found: %r" % (rest,))
                except (KeyError, NoSectionError, NoOptionError):
                    raise InterpolationMissingOptionError(
                        option, section, rest, "/".join(path))
                if "$" in v:
                    self._interpolate_some(parser, opt, accum, v, sect,
                                           dict(parser.items(sect, raw=True)),
                                           depth + 1)
                else:
                    accum.append(v)
            else:
                raise InterpolationSyntaxError(
                    option, section,
                    "'$' must be followed by '$' or '{', "
                    "found: %r" % (rest,))

class UConfigParser(ConfigParser):
    """UConfigParser [class(ConfigParser)]
    UPath:
        Notation: path
        Format: /dir/[file]
    UFilePath:
        Notation: path (file)
        Format: /dir/file
    UDirPath:
        Notation: path (dir)
        Format: /dir/
    
    [NOT RECOMMENDED|DEPRECATED]
    
    Uses Filesystem-like structures in ini-files
    
    [NOTE] Why Not uset() and uget() => set() and get()?
    I cannot put uset() and uget() to the standard set/get methods
    since they practice another Parameter Syntax and get/set are internally used.
    If i wanted to do so i either had to Kill functionality or rewrite the whole class.
    I don't want to do either one.
    
    set/get:
        uset(UFilePath, value, createDir=False)
            UPath setter
        uget*(UFilePath)
            UPath getter
        set(section, option, value)
            Default setter
        get*(section, option)
            Default getter
    *=[,int,float,boolean]"""
    _DEFAULT_INTERPOLATION=UInterpolation()
    #Set functions
    def uset(self, path, value, createDir=False):
        """@ARG string     path (file)
        @ARG string     value
        @ARG boolean    [createDir] False
        @RET boolean    rtn
        @DSC Set path to value
        @DSC if createDir is true it too creates Directories
        @EQA UNIX 'echo $value > $path'"""
        (section, key)=posixpath.split(path)
        if key=="":
            raise UPathError("set(): ["+path+"]: Expected File")
        else:
            if not self.has_section(section):
                if createDir:
                    self.add_section(section)
                else:
                    raise NoSectionError(section)
            return self.set(section, key, value)
    echo = uset
    def touch(self, path, createDir=False):
        """@ARG string     path
        @ARG boolean    [createDir] False
        @DSC implies the Unix touch command
        @DSC if createDir is true it too creates Directories
        @EQA UNIX 'touch'"""
        (section, key)=posixpath.split(path)
        if key=="":
            if not createDir:
                raise UPathError("touch(): ["+path+"]: Expected File")
            else:
                self.add_section(section)
                return
        if not self.has_section(section):
            if createDir:
                self.add_section(section)
            else:
                raise NoSectionError(section)
        if not self.has_option(section, key):
            self.set(section, key, "")
    def create(self, path):
        """@ARG string     path
        @DSC touches/creates file and/or directory if nonexistent
        @EQA THIS 'touch(path, True)'"""
        self.touch(path, True)
    def rm(self, path):
        """@ARG string     path (file)
        @RET boolean    success
        @DSC Removes File
        @EQA UNIX 'rm'"""
        (section, key)=posixpath.split(path)
        if key=="":
            raise UPathError("rm(): ["+path+"]: Expected File")
        else:
            return self.remove_option(section, key)
    def mkdir(self, path):
        """@ARG string     path (dir)
        @RET boolean    success
        @DSC creates new directory
        @EQA UNIX 'mkdir'"""
        if path[-1]==posixpath.sep:
            section=path[:-1]
        else:
            section=path
        return self.add_section(section)
    def rmdir(self, path):
        """@ARG string     path (dir)
        @RET boolean    success
        @DSC Clears (ATTENTION: even non-empty) Directory; no subdirectories
        @EQA [UNIX 'rm -rf']; [UNIX 'rmdir']"""
        (section, key)=posixpath.split(path)
        if key!="":
            raise UPathError("rmdir(): ["+path+"]: Expected Directory")
        else:
            return self.remove_section(section)
    def rmtree(self, path):
        """@ARG string     path (dir)
        @DSC Recursively removes path
        @EQA UNIX 'rm -rf'; DOS 'rmtree'"""
        (section, key)=posixpath.split(path)
        if key!="":
            raise UPathError("rmdir(): ["+path+"]: Expected Directory")
        else:
            for i in self.sections():
                if i[:len(section)]==section:
                    self.remove_section(i)
    def addtree(self, path, tree_dict):
        """@ARG string path (dir)
        @ARG dict   tree_dict
        @DSC Puts dict to path/*"""
        if path[-1]==posixpath.sep:
            section=path[:-1]
        else:
            section=path
        for i in tree_dict.items():
            self.uset(posixpath.join(section, i[0]), i[1],  True)
    #Get functions
    def gettree(self, path):
        """@ARG string     path (dir)
        @RET dict       section
        @DSC get a ini section"""
        section=posixpath.split(path)[0]
        self.__getitem__(section)
    def ls(self, path):
        """@ARG string     path (dir)
        @RET list       contents
        @EQA UNIX 'ls'"""
        if path[-1]==posixpath.sep and path!="/":
            root=path[:-1]
        else:
            root=path
        lst=list()
        cnt=root.count(posixpath.sep)
        for i in self.sections():
            if root=="/":
                if i[0]=="/" and i.count(posixpath.sep)==1:
                    if i[1:] not in lst: lst.append(i[1:])
                else:
                    c=i.split(posixpath.sep)[0]
                    if c not in lst: lst.append(c)
            elif i[:len(root)]==root and cnt<i.count(posixpath.sep):
                c=i.split(posixpath.sep)[cnt+1]
                if c not in lst: lst.append(c)
        if self.has_section(root):
            for i in self.options(root):
                lst.append(i)
        return lst
    def lsr(self, path):
        lst=self.ls(path)
        dct={}
        for i in lst:
            if self.isdir(posixpath.join(path, i, "")):
                dct[i]=self.lsr(posixpath.join(path, i))
            else:
                dct[i]=""
        return dct
    def ls1(self, path):
        """@ARG string     path (dir)
        @RET list       files
        @DSC list files in path
        @EQA UNIX 'find -depth 1 -type f'"""
        if path[-1]==posixpath.sep:
            section=path[:-1]
        else:
            section=path
        return self.options(section)
    def uget(self, path, **kwargs):
        """@ARG string        path (file)
        @ARG boolean       [raw]      False
        @ARG dict          [vars]     {}
        @ARG string        [fallback] ?
        @RET string        value
        @DSC Returns value of path [Last 3 @ARGs are kwarg-only]
        @EQA UNIX 'cat'"""
        (section, key)=posixpath.split(path)
        return super().get(section, key, **kwargs)
    cat = uget
    def ugetint(self, path, **kwargs):
        """@ARG string     path (file)
        @ARG boolean    [raw]         False
        @ARG dict       [vars]        {}
        @ARG integer    [fallback]    ?
        @RET integer    value
        @DSC Returns value of path as integer [Last 3 @ARGs are kwarg-only]"""
        (section, key)=posixpath.split(path)
        return super().getint(section, key, **kwargs)
    def ugetfloat(self, path, **kwargs):
        """@ARG string       path (file)
        @ARG boolean      [raw]       False
        @ARG dict         [vars]      {}
        @ARG float        [fallback]  ?
        @RET float        value
        @DSC Returns value of path as floating-point number [Last 3 @ARGs are kwarg-only]"""
        (section, key)=posixpath.split(path)
        return super().getfloat(section, key, **kwargs)
    def ugetboolean(self, path, **kwargs):
        """@ARG string     path (file)
        @ARG boolean    [raw]         False
        @ARG dict       [vars]        {}
        @ARG boolean    [fallback]    ?
        @RET boolean    value
        @DSC Returns value of path as boolean value [Last 3 @ARGs are kwarg-only]"""
        (section, key)=posixpath.split(path)
        return super().getboolean(section, key, **kwargs)
    #Check Functions
    def exists(self, path):
        """@ARG string     path
        @RET boolean    exists
        @DSC Return True if path is an existing file/directory; otherwise False
        @EQA UNIX 'test -e'"""
        (section, key)=posixpath.split(path)
        if key!="":
            return self.has_option(section, key)
        else:
            return self.has_section(section)
    def isfile(self, path):
        """@ARG string     path
        @RET boolean    is_file
        @DSC Return True if path is an existing file; otherwise False
        @EQA UNIX 'test -f'"""
        (section, key)=posixpath.split(path)
        return key!="" and self.has_section(section) and self.has_option(section, key)
    def isdir(self, path):
        """@ARG string     path
        @RET boolean    is_dir
        @DSC Return True if path is an existing directory; otherwise False"""
        (section, key)=posixpath.split(path)
        return key=="" and self.has_section(section)
