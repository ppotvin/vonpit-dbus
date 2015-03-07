# coding: utf-8
from vonpit_dbus.auth_mechanism import AuthMechanism


class AnonymousAuthMechanism(AuthMechanism):
    def challenge_with(self, challenge):
        return self.ERROR, None

    @property
    def name(self):
        return 'ANONYMOUS'

    def get_initial_response(self):
        return self.OK, None
