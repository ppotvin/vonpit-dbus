# coding: utf-8


class DbusConnection(object):

    def __init__(self, transport):
        super(DbusConnection, self).__init__()
        self.__transport = transport

    def start_client(self):
        self.__transport.send_null_byte()

    def auth(self):
        self.__transport.send_line('AUTH')
        self.__transport.recv_command()
