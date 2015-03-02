# coding: utf-8
import unittest

from mock import MagicMock

from vonpit_dbus.connection import DbusConnectionError

from vonpit_dbus.tests._test_connection import ADbusConnection, TextReplayTransport
from vonpit_dbus.transport import Transport


class DbusConnectionUnitTest(unittest.TestCase):
    def test_when_start_client_should_send_nul_byte(self):
        transport = MagicMock(spec_set=Transport)
        connection = given(ADbusConnection().with_transport(transport))

        connection.start_client()

        transport.send_null_byte.assert_called_once_with()

    def test_when_get_available_mechanisms_should_return_available_mechanisms(self):
        mechanisms = ['KERBEROS_V4', 'SKEY']
        transport = TextReplayTransport('''
        C: AUTH
        S: REJECTED %s
        ''' % ' '.join(mechanisms))
        connection = given(ADbusConnection().connected().with_transport(transport))

        result = connection.get_available_mechanisms()

        transport.assert_story_completed()
        for mechanism in mechanisms:
            self.assertIn(mechanism, result)

    def test_invalid_answer_when_get_available_mechanisms_should_raise_DbusConnectionError(self):
        transport = TextReplayTransport('''
        C: AUTH
        S: REJCETED SKEY
        ''')
        connection = given(ADbusConnection().connected().with_transport(transport))

        with self.assertRaises(DbusConnectionError):
            connection.get_available_mechanisms()

        transport.assert_story_completed()

    def test_error_answer_when_get_available_mechanisms_should_raise_DbusConnectionError(self):
        transport = TextReplayTransport('''
        C: AUTH
        S: ERROR
        ''')
        connection = given(ADbusConnection().connected().with_transport(transport))

        with self.assertRaises(DbusConnectionError):
            connection.get_available_mechanisms()

        transport.assert_story_completed()


def given(builder):
    return builder.build()
