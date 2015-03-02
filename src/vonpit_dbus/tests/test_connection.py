# coding: utf-8
import unittest

from mock import MagicMock

from vonpit_dbus.connection import DbusConnectionError

from vonpit_dbus.tests._test_connection import ADbusConnection
from vonpit_dbus.tests._test_connection import TextReplayTransport
from vonpit_dbus.tests._test_connection import FakeAuthMechanism
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

    def test_when_authenticate_should_use_initial_response_from_mechanism(self):
        a_mechanism_name = 'MAGIC_COOKIE'
        an_initial_response = '3138363935333137393635383634'
        a_guid = '1234deadbeef'
        transport = TextReplayTransport('''
        C: AUTH %s %s
        S: OK %s
        ''' % (a_mechanism_name, an_initial_response, a_guid))
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = FakeAuthMechanism(a_mechanism_name, an_initial_response)

        connection.authenticate_with(mechanism)

        transport.assert_story_completed()

    def test_when_authenticate_should_use_mechanism(self):
        a_mechanism_name = 'SKEY'
        a_guid = '1234deadbeef'
        a_challenge = '8799cabb2ea93e'
        a_response = '8ac876e8f68ee9809bfa876e6f9876g8fa8e76e98f'
        transport = TextReplayTransport('''
        C: AUTH %s
        S: DATA %s
        C: DATA %s
        S: OK %s
        ''' % (a_mechanism_name, a_challenge, a_response, a_guid))
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = FakeAuthMechanism(a_mechanism_name, None, [(a_challenge, a_response)])

        connection.authenticate_with(mechanism)

        transport.assert_story_completed()


def given(builder):
    return builder.build()
