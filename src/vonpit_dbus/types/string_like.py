# coding: utf-8
from vonpit_dbus.types import DbusBasicType


class String(DbusBasicType):
    LENGTH_ALIGNMENT = 4
    CODE = 's'


class ObjectPath(String):
    LENGTH_ALIGNMENT = 4
    CODE = 'o'


class Signature(String):
    LENGTH_ALIGNMENT = 1
    CODE = 'g'
