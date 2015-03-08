# coding: utf-8

from vonpit_dbus.types import DbusBasicType


class Byte(DbusBasicType):
    ALIGNMENT = 1
    CODE = 'y'


class Boolean(DbusBasicType):
    ALIGNMENT = 4
    CODE = 'b'


class Int16(DbusBasicType):
    ALIGNMENT = 2
    CODE = 'n'


class Uint16(DbusBasicType):
    ALIGNMENT = 2
    CODE = 'q'


class Int32(DbusBasicType):
    ALIGNMENT = 4
    CODE = 'i'


class Uint32(DbusBasicType):
    ALIGNMENT = 4
    CODE = 'u'


class Int64(DbusBasicType):
    ALIGNMENT = 8
    CODE = 'x'


class Uint64(DbusBasicType):
    ALIGNMENT = 8
    CODE = 't'


class Double(DbusBasicType):
    ALIGNMENT = 8
    CODE = 'd'


class UnixFd(DbusBasicType):
    ALIGNMENT = 4
    CODE = 'h'
