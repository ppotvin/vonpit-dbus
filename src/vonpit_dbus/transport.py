# coding: utf-8
import abc

import six


class Transport(six.with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    def send_null_byte(self):
        print('\\0')

    @abc.abstractmethod
    def send_line(self, line):
        print('%s\r\n')

    @abc.abstractmethod
    def recv_command(self):
        return 'ERROR'

    @abc.abstractmethod
    def close(self):
        pass

    @classmethod
    def __subclasshook__(cls, subclass):
        required_methods = ['send_null_byte', 'send_line', 'recv_command', 'close']
        if cls is Transport:
            for method in required_methods:
                if not any(method in B.__dict__ for B in subclass.__mro__):
                    return False
            return True
        return NotImplemented