#http://gist.github.com/1333605
#
# Copyright (c) 2011 Daniel Gerber.
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Regular expressions for URI (rfc3896) and IRI (rfc3987) validation.

    >>> import regex
    >>> u = regex.compile('^%s$' % patterns['URI'])
    >>> m = u.match(u'http://tools.ietf.org/html/rfc3986#appendix-A')
    >>> assert m.groupdict() == {u'scheme': u'http',
    ...                          u'authority': u'tools.ietf.org',
    ...                          u'userinfo': None, u'host': u'tools.ietf.org',
    ...                          u'port': None, u'path': u'/html/rfc3986',
    ...                          u'query': None, u'fragment': u'appendix-A'}
    >>> assert not u.match(u'urn:\U00010300')
    >>> assert regex.match('^%s$' % patterns['IRI'], u'urn:\U00010300')
    >>> assert not regex.match('^%s$' % patterns['relative_ref'], '#f#g')

"""

try:
    import regex #@UnusedImport
except ImportError:
    import logging
    logging.getLogger(__name__).\
    warning('Could not import regex. The stdlib re (at least until python 3.2) '
          'cannot compile the regular expressions in this module (reusing '
          'capture group names on different branches of an alternation).')
    HAS_REGEX = False
else:
    HAS_REGEX = True

__all__ = ('UriRegex')


_common_rules = (

    ########   SCHEME   ########
    ('scheme',        "(?P<scheme>[a-zA-Z][a-zA-Z0-9+.-]*)"),            #named

    ########   PORT   ########
    ('port',          "(?P<port>[0-9]*)"),                               #named

    ########   IP ADDRESSES   ########
    ('IP_literal',  r"\[(?:{IPv6address}|{IPvFuture})\]"),
    ('IPv6address', ("                                (?:{h16}:){{6}} {ls32}"
                     "|                            :: (?:{h16}:){{5}} {ls32}"
                     "|                    {h16}?  :: (?:{h16}:){{4}} {ls32}"
                     "| (?:(?:{h16}:)?     {h16})? :: (?:{h16}:){{3}} {ls32}"
                     "| (?:(?:{h16}:){{,2}}{h16})? :: (?:{h16}:){{2}} {ls32}"
                     "| (?:(?:{h16}:){{,3}}{h16})? :: (?:{h16}:)      {ls32}"
                     "| (?:(?:{h16}:){{,4}}{h16})? ::                 {ls32}"
                     "| (?:(?:{h16}:){{,5}}{h16})? ::                 {h16} "
                     "| (?:(?:{h16}:){{,6}}{h16})? ::                       "
                     ).replace(' ', '')),
    ('ls32',         "(?:{h16}:{h16}|{IPv4address})"),
    ('h16',          "[0-9A-F]{{1,4}}"),
    ('IPv4address', r"(?:(?:{dec_octet}\.){{3}}{dec_octet})"),
    ('dec_octet',    "(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)"),
    ('IPvFuture',   r"v[0-9A-F]+\.(?:{unreserved}|{sub_delims}|:)+"),

    ########  CHARACTER CLASSES   ########
    ('unreserved',    "[a-zA-Z0-9_.~-]"),
    ('reserved',      "(?:{gen_delims}|{sub_delims})"),
    ('pct_encoded',  r"%[0-9A-F][0-9A-F]"),
    ('gen_delims',   r"[:/?#[\]@]"),
    ('sub_delims',    "[!$&'()*+,;=]"),

)


_uri_rules = (

    ########   REFERENCES   ########    
    ('URI_reference',   "{URI}|{relative_ref}"),
    ('URI',             r"{absolute_URI}(?:\#{fragment})?"),
    ('absolute_URI',    r"{scheme}:{hier_part}(?:\?{query})?"),
    ('relative_ref',   ("(?:{relative_part}"
                        r"(?:\?{query})?(?:\#{fragment})?)")),
    
    ('hier_part',      ("(?://{authority}{path_abempty}"
                        "|{path_absolute}|{path_rootless}|{path_empty})")),
    ('relative_part',  ("(?://{authority}{path_abempty}"
                        "|{path_absolute}|{path_noscheme}|{path_empty})")),
    
    ########   AUTHORITY   ########
    ('authority',("(?P<authority>"                                       #named
                  "(?:{userinfo}@)?{host}(?::{port})?)")),
    ('host',      "(?P<host>{IP_literal}|{IPv4address}|{reg_name})"),    #named
    ('userinfo', ("(?P<userinfo>"                                        #named
                  "(?:{unreserved}|{pct_encoded}|{sub_delims}|:)*)")),
    ('reg_name',  "(?:{unreserved}|{pct_encoded}|{sub_delims})*"),
    
    ########   PATH   ########
    ('path',         ("{path_abempty}|{path_absolute}|{path_noscheme}"
                      "|{path_rootless}|{path_empty}")),
    ('path_abempty',  "(?P<path>(?:/{segment})*)"),                      #named
    ('path_absolute', "(?P<path>/(?:{segment_nz}(?:/{segment})*)?)"),    #named
    ('path_noscheme', "(?P<path>{segment_nz_nc}(?:/{segment})*)"),       #named
    ('path_rootless', "(?P<path>{segment_nz}(?:/{segment})*)"),          #named
    ('path_empty',    "(?P<path>)"),                                     #named
    
    ('segment',       "{pchar}*"),
    ('segment_nz',    "{pchar}+"),
    ('segment_nz_nc', "(?:{unreserved}|{pct_encoded}|{sub_delims}|@)+"),
    
    ########   QUERY   ########
    ('query',         r"(?P<query>(?:{pchar}|/|\?)*)"),                  #named
    
    ########   FRAGMENT   ########
    ('fragment',      r"(?P<fragment>(?:{pchar}|/|\?)*)"),               #named
    
    ########  CHARACTER CLASSES   ########
    ('pchar',         "(?:{unreserved}|{pct_encoded}|{sub_delims}|:|@)"),
    ('unreserved',    "[a-zA-Z0-9._~-]"),

)


#: http://tools.ietf.org/html/rfc3987
#: January 2005
_iri_rules = (

    ########   REFERENCES   ########
    ('IRI_reference',   "{IRI}|{irelative_ref}"),
    ('IRI',             r"{absolute_IRI}(?:\#{ifragment})?"),
    ('absolute_IRI',    r"{scheme}:{ihier_part}(?:\?{iquery})?"),
    ('irelative_ref',  ("(?:{irelative_part}"
                        r"(?:\?{iquery})?(?:\#{ifragment})?)")),

    ('ihier_part',     ("(?://{iauthority}{ipath_abempty}"
                        "|{ipath_absolute}|{ipath_rootless}|{ipath_empty})")),
    ('irelative_part', ("(?://{iauthority}{ipath_abempty}"
                        "|{ipath_absolute}|{ipath_noscheme}|{ipath_empty})")),


    ########   AUTHORITY   ########
    ('iauthority',("(?P<iauthority>"                                     #named
                   "(?:{iuserinfo}@)?{ihost}(?::{port})?)")),
    ('iuserinfo', ("(?P<iuserinfo>"                                      #named
                   "(?:{iunreserved}|{pct_encoded}|{sub_delims}|:)*)")),
    ('ihost',      "(?P<ihost>{IP_literal}|{IPv4address}|{ireg_name})"), #named
    
    ('ireg_name',  "(?:{iunreserved}|{pct_encoded}|{sub_delims})*"),
    
    ########   PATH   ########
    ('ipath',         ("{ipath_abempty}|{ipath_absolute}|{ipath_noscheme}"
                       "|{ipath_rootless}|{ipath_empty}")),

    ('ipath_empty',    "(?P<ipath>)"),                                   #named
    ('ipath_rootless', "(?P<ipath>{isegment_nz}(?:/{isegment})*)"),      #named
    ('ipath_noscheme', "(?P<ipath>{isegment_nz_nc}(?:/{isegment})*)"),   #named
    ('ipath_absolute', "(?P<ipath>/(?:{isegment_nz}(?:/{isegment})*)?)"),#named
    ('ipath_abempty',  "(?P<ipath>(?:/{isegment})*)"),                   #named
    
    ('isegment_nz_nc', "(?:{iunreserved}|{pct_encoded}|{sub_delims}|@)+"),
    ('isegment_nz',    "{ipchar}+"),
    ('isegment',       "{ipchar}*"),
    
    ########   QUERY   ########
    ('iquery',    r"(?P<iquery>(?:{ipchar}|{iprivate}|/|\?)*)"),         #named
    
    ########   FRAGMENT   ########
    ('ifragment', r"(?P<ifragment>(?:{ipchar}|/|\?)*)"),                 #named

    ########   CHARACTER CLASSES   ########
    ('ipchar',      "(?:{iunreserved}|{pct_encoded}|{sub_delims}|:|@)"),
    ('iunreserved', "(?:[a-zA-Z0-9._~-]|{ucschar})"),
    ('iprivate', "[\uE000-\uF8FF\U000F0000-\U000FFFFD\U00100000-\U0010FFFD]"),
    ('ucschar', ("[\xA0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF"
                 "\U00010000-\U0001FFFD\U00020000-\U0002FFFD"
                 "\U00030000-\U0003FFFD\U00040000-\U0004FFFD"
                 "\U00050000-\U0005FFFD\U00060000-\U0006FFFD"
                 "\U00070000-\U0007FFFD\U00080000-\U0008FFFD"
                 "\U00090000-\U0009FFFD\U000A0000-\U000AFFFD"
                 "\U000B0000-\U000BFFFD\U000C0000-\U000CFFFD"
                 "\U000D0000-\U000DFFFD\U000E1000-\U000EFFFD]")),
    
)


class UriRegex(object):
    instance = None
    patterns = {}
    
    @classmethod
    def __makepatterns(klass):
        #: mapping of rfc3986 / rfc3987 rule names to regular expressions
        for name, rule in _common_rules[::-1] + _uri_rules[::-1] + _iri_rules[::-1]:
            klass.patterns[name] = rule.format(**klass.patterns)
        del name, rule
    
    @classmethod
    def getInstance(klass):
        if klass.instance is None:
            klass.instance = klass()
        return klass.instance
    
    def __init__(self):
        if (not HAS_REGEX):
            logging.getLogger(__name__).\
            error("Cannot compile patterns. Please install the regex module from PyPI.")
        
        self.uri = regex.compile(self.patterns["URI"])
        self.iri = regex.compile(self.patterns["IRI"])
        self.uriMatch = regex.compile("^{0}$".format(self.patterns["URI"]))
        self.iriMatch = regex.compile("^{0}$".format(self.patterns["IRI"]))
        
    def isUri(self, string):
        """Check for URI (rfc3896) Validity"""
        return bool(self.uriMatch.match(string))
    
    def isIri(self, string):
        """Check for IRI (rfc3987) Validity"""
        return bool(self.iriMatch.match(string))

UriRegex._UriRegex__makepatterns()
