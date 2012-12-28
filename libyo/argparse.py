"""
----------------------------------------------------------------------
- argparse: ArgumentParser additions
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

try: #Python 2.7+, Python 3.2+
    from argparse import ArgumentParser as StockArgumentParser #@UnusedImport
except ImportError:
    pass

from .extern.argparse import ArgumentParser, HelpFormatter, RawDescriptionHelpFormatter, RawTextHelpFormatter, ArgumentDefaultsHelpFormatter #@UnusedImport
from .extern.argparse import ArgumentError, ArgumentTypeError #@UnusedImport
from .extern.argparse import Action, FileType, Namespace #@UnusedImport
from .extern.argparse import SUPPRESS, OPTIONAL, ZERO_OR_MORE, ONE_OR_MORE, PARSER, REMAINDER #@UnusedImport
import sys as _sys


class ArgumentParserExit(Exception):
    def __init__(self, status, message):
        super(ArgumentParserExit, self).__init__(message)
        self.status = status


class LibyoArgumentParser(ArgumentParser):
    """Extended Version of ArgumentParser v1.2
        to improve the coder's control over Output and exiting policies.

    Keyword Arguments:
        - prog -- The name of the program (default: sys.argv[0])
        - usage -- A usage message (default: auto-generated from arguments)
        - description -- A description of what the program does
        - epilog -- Text following the argument descriptions
        - version -- DEPPRECATED!
        - parents -- Parsers whose arguments should be copied into this one
        - formatter_class -- HelpFormatter class for printing help messages
        - prefix_chars -- Characters that prefix optional arguments
        - fromfile_prefix_chars -- Characters that prefix files containing
            additional arguments
        - argument_default -- The default value for all arguments
        - conflict_handler -- String indicating how to handle conflicts
        - add_help -- Add a -h/--help option
        - may_exit -- [BOOL] Wether or not LibyoArgumentParser is allowed to use
            sys.exit
        - autoprint_usage -- [BOOL] Wether or not LibyoArgumentParser should print
            the Usage screen on errors.
        - autoprint_message -- [BOOL] Wether or not LibyoArgumentParser should print
            Error Messages.
        - output_handle -- [FILE] The Filehandle to use for output
        - error_handle -- [FILE] The Filehandle to use for error messages (if enabled above)
    """
    def __init__(self,
                 prog=None,
                 usage=None,
                 description=None,
                 epilog=None,
                 version=None,
                 parents=[],
                 formatter_class=HelpFormatter,
                 prefix_chars='-',
                 fromfile_prefix_chars=None,
                 argument_default=None,
                 conflict_handler='error',
                 add_help=True,
                 may_exit=True,
                 autoprint_usage=True,
                 autoprint_message=True,
                 output_handle=_sys.stdout,
                 error_handle=_sys.stderr):
        super(LibyoArgumentParser, self).__init__(prog, usage, description, epilog, version, parents,
                                            formatter_class, prefix_chars, fromfile_prefix_chars,
                                            argument_default, conflict_handler, add_help)
        self.may_exit = may_exit
        self.autoprint_usage = autoprint_usage
        self.autoprint_message = autoprint_message
        self.output_handle = output_handle
        self.error_handle = error_handle
    
    # =====================
    # Help-printing methods
    # =====================
    def print_usage(self, fp=None):
        if fp is None:
            fp = self.output_handle
        self._print_message(self.format_usage(), fp)
    
    def print_help(self, fp=None):
        if fp is None:
            fp = self.output_handle
        self._print_message(self.format_help(), fp)
    
    def print_version(self, fp=None):
        import warnings
        warnings.warn(
            'The print_version method is deprecated -- the "version" '
            'argument to ArgumentParser is no longer supported.',
            DeprecationWarning)
        self._print_message(self.format_version(), fp)
    
    def _print_message(self, message, fp=None):
        if fp is None:
            fp = self.output_handle
        fp.write(message)
    
    # ===============
    # Exiting methods
    # ===============
    def exit(self, status=0, message=None): #@ReservedAssignment
        if self.autoprint_message and message is not None:
                self._print_message(message, self.error_handle)
        if self.may_exit:
            _sys.exit(status)
        else:
            raise ArgumentParserExit(status, message)
    
    def error(self, message):
        if self.autoprint_usage:
            self.print_usage(self.error_handle)
        self.exit("{prog}: error: {message}".format(prog=self.prog, message=message))
