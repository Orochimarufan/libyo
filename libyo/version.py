"""
@author Orochimarufan
@module libyo.version
@created 2012-03-07
@modified 2012-05-04
"""

from __future__ import absolute_import, unicode_literals, division

from . import __VERSION__ as LIBYO_VERSION_TUPLE
from . import LIBYO_VERSION, LIBYO_VERSION_MAJOR, LIBYO_VERSION_MINOR, LIBYO_VERSION_MICRO, LIBYO_VERSION_PATCH #@UnusedImports
from .reflect.property import classproperty
from sys import version_info as PY_VERSION_INFO
PY_VERSION_MAJOR=PY_VERSION_INFO[0]
PY_VERSION_MINOR=PY_VERSION_INFO[1]
PY_VERSION_MICRO=PY_VERSION_INFO[2]
PY_VERSION_PATCH=""
PY_VERSION_TUPLE=tuple(PY_VERSION_INFO[:3])+("",)
PY_VERSION_LEVEL=PY_VERSION_INFO[3]

class Version(object):
    class OutdatedError(Exception):
        FORMAT_FORMESG="{1}.Version.OutdatedError: {0}"
        FORMAT_MESSAGE="'{0}' is outdated:\r\n\xA0\xA0\xA0\xA0This Application requires {0} v{1} (You are currently running v{2})\r\n\xA0\xA0\xA0\xA0Please upgrade {0} to version {1} or newer."
        def __init__(self,componentName,reqVersionTuple,insVersionTuple):
            self.component_name=componentName;
            self.required_version=reqVersionTuple;
            self.required_version_string=Version._format_version(reqVersionTuple);
            self.installed_version=insVersionTuple;
            self.installed_version_string=Version._format_version(insVersionTuple);
            super(Version.OutdatedError,self).__init__(self.FORMAT_MESSAGE.format(
                                                            self.component_name,self.required_version_string,
                                                            self.installed_version_string));
        @classmethod
        def format_message(cls,componentName,reqVersionTuple,insVersionTuple):
            return cls.FORMAT_FORMESG.format(cls.FORMAT_MESSAGE.format(
                                                componentName,Version._format_version(reqVersionTuple),
                                                Version._format_version(insVersionTuple)),
                                             cls.__module__);
    def __init__(self,componentName,major,minor=0,micro=0,patch=""):
        self.version=self.versionTuple(major, minor, micro, patch);
        self.name=componentName;
    @classproperty
    def LibyoVersion(cls):
        return cls._libyo_version()
    @classmethod
    def _libyo_version(cls):
        if not hasattr(cls,"__libyo_instance__"):
            cls.__libyo_instance__=cls("libyo",LIBYO_VERSION_TUPLE);
        return cls.__libyo_instance__;
    @classproperty
    def PythonVersion(cls):
        return cls._python_version()
    @classmethod
    def _python_version(cls):
        if not hasattr(cls,"__python_instance__"):
            cls.__python_instance__=cls("python",PY_VERSION_TUPLE);
        return cls.__python_instance__;
    def _format_self_ver(self):
        return self._format_version(self.version);
    @staticmethod
    def _format_version(version_tuple):
        return "{0}.{1}.{2}{3}".format(*version_tuple)
    @classmethod
    def formatVersion(self,major,minor=0,micro=0,patch=""):
        return self._format_version(self.versionTuple(major, minor, micro, patch));
    def format(self):
        return self._format_self_ver()
    def versionTuple(self,major,minor=0,micro=0,patch=""):
        patch=str(patch).lower();
        if isinstance(major,tuple):
            return major;
        elif isinstance(major,list):
            return tuple(major);
        else:
            return(major,minor,micro,patch);
    def minVersion(self,major,minor=0,micro=0,patch=""):
        tupl=self.versionTuple(major, minor, micro, patch);
        return self.version >= tupl;
    def requireVersion(self,major,minor=0,micro=0,patch=""):
        if not self.minVersion(major, minor, micro, patch):
            tupl=self.versionTuple(major, minor, micro, patch);
            raise Version.OutdatedError(self.name,tupl,self.version);
        return True;
    def fancyRequireVersion(self,major,minor=0,micro=0,patch=""):
        if not self.minVersion(major, minor, micro, patch):
            tupl=self.versionTuple(major, minor, micro, patch);
            print(Version.OutdatedError.format_message(self.name, tupl, self.version));
            raise SystemExit(128);
    def __str__(self):
        return "<Component '{0}' Version {1}>".format(self.name,self._format_self_ver())
    def __repr__(self):
        return "{0}.{1}({2},{3},{4},{5},{6})".format(self.__class__.__module__,self.__class__.__name__,self.name,*self.version)