# coding: utf-8
import abc
import unittest
from unittest.mock import MagicMock

import six

from vonpit_dbus.connection import DbusConnection


class DbusConnectionUnitTest(unittest.TestCase):
    def test_start_client_should_send_nul_byte(self):
        transport = MagicMock(spec_set=Transport)
        DbusConnection(transport).start_client()
        transport.send_null_byte.assert_called_once_with()


class Transport(six.with_metaclass(abc.ABCMeta, object)):
    @abc.abstractmethod
    def send_null_byte(self):
        print('\\0')

    @classmethod
    def __subclasshook__(cls, subclass):
        required_methods = ['send_null_byte']
        if cls is Transport:
            for method in required_methods:
                if not any(method in B.__dict__ for B in subclass.__mro__):
                    return False
            return True
        return NotImplemented
