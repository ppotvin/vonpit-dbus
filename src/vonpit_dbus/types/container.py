# coding: utf-8


class Array(object):
    CODE = 'a'
    LENGTH_ALIGNMENT = 4


class Struct(object):
    CODE = 'r'
    ALIGNMENT = 8

    def __init__(self, enclosed_types):
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
