# coding: utf-8
import unittest

from vonpit_dbus.auth_mechanism import AuthMechanism
from vonpit_dbus.auth_mechanism.anonymous import AnonymousAuthMechanism


class AnonymousAuthMechanismUnitTest(unittest.TestCase):
    def test_when_name_should_return_anonymous(self):
        mechanism = AnonymousAuthMechanism()
        result = mechanism.name
        self.assertTrue(result, 'ANONYMOUS')

    def test_when_get_initial_response_should_return_nothing(self):
        mechanism = AnonymousAuthMechanism()
        result = mechanism.get_initial_response()
        self.assertEqual(result, (AuthMechanism.OK, None))

    def test_should_be_an_auth_mechanism(self):
        mechanism = AnonymousAuthMechanism()
        self.assertIsInstance(mechanism, AuthMechanism)
