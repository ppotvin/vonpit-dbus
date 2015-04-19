# coding: utf-8
import struct

from vonpit_dbus.types import DbusBasicType


class DbusFixedType(DbusBasicType):
    @classmethod
    def pack(cls, value, endianness):
        return struct.pack('%s%s' % (endianness, cls._STRUCT_FORMAT), value)


class Byte(DbusFixedType):
    ALIGNMENT = 1
    CODE = 'y'
    _STRUCT_FORMAT = 'b'


class Boolean(DbusFixedType):
    ALIGNMENT = 4
    CODE = 'b'
    _STRUCT_FORMAT = 'L'


class Int16(DbusFixedType):
    ALIGNMENT = 2
    CODE = 'n'
    _STRUCT_FORMAT = 'h'


class Uint16(DbusFixedType):
    ALIGNMENT = 2
    CODE = 'q'
    _STRUCT_FORMAT = 'H'


class Int32(DbusFixedType):
    ALIGNMENT = 4
    CODE = 'i'
    _STRUCT_FORMAT = 'l'


class Uint32(DbusFixedType):
    ALIGNMENT = 4
    CODE = 'u'
    _STRUCT_FORMAT = 'L'


class Int64(DbusFixedType):
    ALIGNMENT = 8
    CODE = 'x'
    _STRUCT_FORMAT = 'q'


class Uint64(DbusFixedType):
    ALIGNMENT = 8
    CODE = 't'
    _STRUCT_FORMAT = 'Q'


class Double(DbusFixedType):
    ALIGNMENT = 8
    CODE = 'd'
    _STRUCT_FORMAT = 'd'


class UnixFd(DbusFixedType):
    ALIGNMENT = 4
    CODE = 'h'
    _STRUCT_FORMAT = 'L'
