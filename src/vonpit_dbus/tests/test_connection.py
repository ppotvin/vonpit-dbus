# coding: utf-8
import unittest

from mock import MagicMock

from vonpit_dbus.connection import DbusConnectionError, DbusAuthenticationFailure
from vonpit_dbus.tests._test_connection import ADbusConnection
from vonpit_dbus.tests._test_connection import AFakeAuthMechanism
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
        self.assertEqual(len(mechanisms), len(result))

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
        transport = TextReplayTransport('''
        C: AUTH %s %s
        S: OK universal_id
        ''' % (a_mechanism_name, an_initial_response))
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = FakeAuthMechanism(a_mechanism_name, an_initial_response)

        connection.authenticate_with(mechanism)

        transport.assert_story_completed()


class DbusConnectionClientAuthenticationTest(unittest.TestCase):
    def test_waiting_for_data_when_receive_data_should_challenge_mechanism(self):
        a_challenge = ('8799cabb2ea93e', '8ac876e8f68ee9809bfa876e6f9876g8fa8e76e98f')
        transport = TextReplayTransport('''
        C: AUTH %s
        S: DATA %s
        C: DATA %s
        S: OK universal_id
        ''' % (AFakeAuthMechanism.NAME, a_challenge[0], a_challenge[1]))
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism().with_challenges([a_challenge]))

        connection.authenticate_with(mechanism)

        transport.assert_story_completed()

    def test_waiting_for_data_when_receive_rejected_should_raise_DbusAuthenticationFailure(self):
        another_mechanism = 'MAGIC_COOKIE'
        transport = TextReplayTransport('''
        C: AUTH %s
        S: REJECTED %s
        ''' % (AFakeAuthMechanism.NAME, another_mechanism))
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism().with_any_challenge())

        with self.assertRaises(DbusAuthenticationFailure):
            connection.authenticate_with(mechanism)

        transport.assert_story_completed()

    def test_waiting_for_data_when_receive_error_should_send_cancel_and_wait_for_reject(self):
        transport = TextReplayTransport('''
        C: AUTH %s
        S: ERROR
        C: CANCEL
        S: REJECTED
        ''' % AFakeAuthMechanism.NAME)
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism().with_any_challenge())

        with self.assertRaises(DbusAuthenticationFailure):
            connection.authenticate_with(mechanism)

        transport.assert_story_completed()

    def test_waiting_for_data_when_receive_ok_should_set_authenticated(self):
        transport = TextReplayTransport('''
        C: AUTH %s
        S: OK universal_id
        ''' % AFakeAuthMechanism.NAME)
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism().with_any_challenge())

        connection.authenticate_with(mechanism)

        transport.assert_story_completed()
        self.assertTrue(connection.authenticated)

    def test_waiting_for_data_when_receive_anything_else_should_send_error_and_wait_for_data(self):
        a_challenge = ('8799cabb2ea93e', '8ac876e8f68ee9809bfa876e6f9876g8fa8e76e98f')
        transport = TextReplayTransport('''
        C: AUTH %s
        S: HELLO
        C: ERROR
        S: DATA %s
        C: DATA %s
        S: OK universal_id
        ''' % (AFakeAuthMechanism.NAME, a_challenge[0], a_challenge[1]))
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism().with_challenges([a_challenge]))

        connection.authenticate_with(mechanism)

        transport.assert_story_completed()

    def test_waiting_for_ok_when_receive_ok_should_set_authenticated(self):
        transport = TextReplayTransport('''
        C: AUTH %s
        S: OK universal_id
        ''' % AFakeAuthMechanism.NAME)
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism())

        connection.authenticate_with(mechanism)

        transport.assert_story_completed()
        self.assertTrue(connection.authenticated)

    def test_waiting_for_ok_when_receive_rejected_should_raise_DbusAuthenticationFailure(self):
        transport = TextReplayTransport('''
        C: AUTH %s
        S: REJECTED
        ''' % AFakeAuthMechanism.NAME)
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism())

        with self.assertRaises(DbusAuthenticationFailure):
            connection.authenticate_with(mechanism)

        transport.assert_story_completed()

    def test_waiting_for_ok_when_receive_data_should_send_cancel_and_wait_for_reject(self):
        transport = TextReplayTransport('''
        C: AUTH %s
        S: DATA some-challenge
        C: CANCEL
        S: REJECTED
        ''' % AFakeAuthMechanism.NAME)
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism())

        with self.assertRaises(DbusAuthenticationFailure):
            connection.authenticate_with(mechanism)

        transport.assert_story_completed()

    def test_waiting_for_ok_when_receive_error_should_send_cancel_and_wait_for_reject(self):
        transport = TextReplayTransport('''
        C: AUTH %s
        S: ERROR msg
        C: CANCEL
        S: REJECTED
        ''' % AFakeAuthMechanism.NAME)
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism())

        with self.assertRaises(DbusAuthenticationFailure):
            connection.authenticate_with(mechanism)

        transport.assert_story_completed()

    def test_waiting_for_ok_when_receive_anything_else_should_send_error_and_wait_for_ok(self):
        transport = TextReplayTransport('''
        C: AUTH %s
        S: BONJOUR
        C: ERROR
        S: OK universal_id
        ''' % AFakeAuthMechanism.NAME)
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism())

        connection.authenticate_with(mechanism)

        transport.assert_story_completed()
        self.assertTrue(connection.authenticated)

    def test_waiting_for_reject_when_receive_anything_else_should_raise_DbusConnectionError_and_disconnect(self):
        transport = TextReplayTransport('''
        C: AUTH %s
        S: ERROR msg
        C: CANCEL
        S: HELLOWHOISTHERE
        ''' % AFakeAuthMechanism.NAME)
        connection = given(ADbusConnection().connected().with_transport(transport))
        mechanism = given(AFakeAuthMechanism())

        with self.assertRaises(DbusConnectionError):
            connection.authenticate_with(mechanism)

        transport.assert_closed()


def given(builder):
    return builder.build()
