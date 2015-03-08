# coding: utf-8
from vonpit_dbus.types import DbusBasicType


class Array(object):
    CODE = 'a'
    LENGTH_ALIGNMENT = 4

    def __init__(self, enclosed_type):
        if not enclosed_type:
            raise ValueError
        self.__enclosed_type = enclosed_type

    @property
    def enclosed_type(self):
        return self.__enclosed_type


class Struct(object):
    CODE = 'r'
    ALIGNMENT = 8

    def __init__(self, enclosed_types):
        if not enclosed_types:
            raise ValueError
        self.__enclosed_types = tuple(enclosed_types)

    @property
    def enclosed_types(self):
        return self.__enclosed_types


class Variant(object):
    CODE = 'v'
    ALIGNMENT = 1


class DictEntry(object):
    CODE = 'e'
    ALIGNMENT = 8

    def __init__(self, key_type, value_type):
        if not isinstance(key_type, DbusBasicType):
            raise ValueError
        self.__key_type = key_type
        self.__value_type = value_type

    @property
    def key_type(self):
        return self.__key_type

    @property
    def value_type(self):
        return self.__value_type
