# coding: utf-8
import abc
import unittest

import six

from mock import MagicMock

from vonpit_dbus.tests._test_connection import ADbusConnection


class DbusConnectionUnitTest(unittest.TestCase):
    def test_start_client_should_send_nul_byte(self):
        transport = MagicMock(spec_set=Transport)
        connection = given(ADbusConnection().with_transport(transport))

        connection.start_client()

        transport.send_null_byte.assert_called_once_with()

    def test_auth_should_send_line(self):
        transport = MagicMock(spec_set=Transport)
        connection = given(ADbusConnection().connected().with_transport(transport))

        connection.auth()

        transport.send_line.assert_called_once_with('AUTH')

    def test_auth_should_wait_for_answer(self):
        transport = MagicMock(spec_set=Transport)
        connection = given(ADbusConnection().connected().with_transport(transport))

        connection.auth()

        transport.recv_command.assert_called_once_with()


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

    @classmethod
    def __subclasshook__(cls, subclass):
        required_methods = ['send_null_byte']
        if cls is Transport:
            for method in required_methods:
                if not any(method in B.__dict__ for B in subclass.__mro__):
                    return False
            return True
        return NotImplemented


def given(builder):
    return builder.build()
