# coding: utf-8


class String(object):
    LENGTH_ALIGNMENT = 4
    CODE = 's'


class ObjectPath(String):
    LENGTH_ALIGNMENT = 4
    CODE = 'o'


class Signature(String):
    LENGTH_ALIGNMENT = 1
    CODE = 'g'
