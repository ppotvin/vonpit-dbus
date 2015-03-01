# coding: utf-8
from vonpit_dbus.connection import DbusConnection


class ADbusConnection(object):
    def __init__(self):
        self.__transport = None
        self.__connected = False

    def connected(self):
        self.__connected = True
        return self

    def with_transport(self, transport):
        self.__transport = transport
        return self

    def build(self):
        connection = DbusConnection(self.__transport)
        if self.__connected:
            connection.start_client()
        return connection