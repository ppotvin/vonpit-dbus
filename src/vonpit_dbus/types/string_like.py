# coding: utf-8
import struct

import six

from vonpit_dbus.types import DbusBasicType


class String(DbusBasicType):
    LENGTH_ALIGNMENT = 4
    CODE = 's'

    @classmethod
    def pack(cls, value, endianness):
        raw_bytes = value if isinstance(value, six.binary_type) else value.encode('utf-8')
        size = len(raw_bytes)
        struct_format = '%sL%dsB' % (endianness, size)
        print(struct_format)
        return struct.pack(struct_format, size, raw_bytes, 0)


class ObjectPath(String):
    LENGTH_ALIGNMENT = 4
    CODE = 'o'


class Signature(String):
    LENGTH_ALIGNMENT = 1
    CODE = 'g'

    @classmethod
    def pack(cls, value, endianness):
        raw_bytes = value if isinstance(value, six.binary_type) else value.encode('utf-8')
        size = len(raw_bytes)
        struct_format = '%sB%dsB' % (endianness, size)
        return struct.pack(struct_format, size, raw_bytes, 0)
