# coding: utf-8
import six


class DbusTypeMeta(type):
    @property
    def alignment(cls):
        return cls.alignment


class Byte(six.with_metaclass(DbusTypeMeta)):
    ALIGNMENT = 1
    CODE = 'y'


class Boolean(six.with_metaclass(DbusTypeMeta)):
    ALIGNMENT = 4
    CODE = 'b'


class Int16(six.with_metaclass(DbusTypeMeta)):
    ALIGNMENT = 2
    CODE = 'n'


class Uint16(six.with_metaclass(DbusTypeMeta)):
    ALIGNMENT = 2
    CODE = 'q'


class Int32(six.with_metaclass(DbusTypeMeta)):
    ALIGNMENT = 4
    CODE = 'i'


class Uint32(six.with_metaclass(DbusTypeMeta)):
    ALIGNMENT = 4
    CODE = 'u'


class Int64(six.with_metaclass(DbusTypeMeta)):
    ALIGNMENT = 8
    CODE = 'x'


class Uint64(six.with_metaclass(DbusTypeMeta)):
    ALIGNMENT = 8
    CODE = 't'


class Double(six.with_metaclass(DbusTypeMeta)):
    ALIGNMENT = 8
    CODE = 'd'


class UnixFd(six.with_metaclass(DbusTypeMeta)):
    ALIGNMENT = 4
    CODE = 'h'
