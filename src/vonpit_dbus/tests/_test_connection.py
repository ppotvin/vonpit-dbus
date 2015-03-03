# coding: utf-8
from vonpit_dbus.auth_mechanism import AuthMechanism
from vonpit_dbus.connection import DbusConnection
from vonpit_dbus.transport import Transport


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


class TextReplayTransport(Transport):
    def __init__(self, story):
        self.__story_lines = story.strip().split('\n')
        self.__story_lines = [line.strip() for line in self.__story_lines]
        self.__line_pointer = 0
        self.__null_byte_sent = False
        self.__closed = False

    def send_null_byte(self):
        if self.__null_byte_sent:
            raise AssertionError('Null byte sent two times')
        self.__null_byte_sent = True

    def send_line(self, line):
        self.check_for_null_byte()
        expected_story_line = self.__story_lines[self.__line_pointer]
        if not expected_story_line.startswith('C: '):
            error_message = 'C: %s != %s' % (line, expected_story_line)
            raise AssertionError(
                'Client sent an unexpected message at line %d: %s' % (self.__line_pointer, error_message)
            )
        if not expected_story_line[3:] == line:
            error_message = '%s != %s' % (line, expected_story_line[3:])
            raise AssertionError(
                'Client sent an unexpected message at line %d: %s' % (self.__line_pointer, error_message)
            )
        self.__line_pointer += 1

    def check_for_null_byte(self):
        if not self.__null_byte_sent:
            raise AssertionError('Null byte was not sent by client')

    def recv_command(self):
        self.check_for_null_byte()
        expected_story_line = self.__story_lines[self.__line_pointer]
        if not expected_story_line.startswith('S: '):
            raise AssertionError(
                'Client requested a answer unexpectedly at line %d: %s' % (self.__line_pointer, expected_story_line)
            )
        self.__line_pointer += 1
        return expected_story_line[3:]

    def assert_story_completed(self):
        if self.__line_pointer != len(self.__story_lines):
            raise AssertionError(
                'Story was not completed: was still waiting for \n'
                '  %s' % '\n  '.join(self.__story_lines[self.__line_pointer:])
            )

    def close(self):
        self.__closed = True

    def assert_closed(self):
        if not self.__closed:
            raise AssertionError('Transport was not closed')


class FakeAuthMechanism(AuthMechanism):
    def __init__(self, name, initial_response, challenges=()):
        self.__name = name
        self.__initial_response = initial_response
        self.__challenges = challenges
        self.__challenge_pointer = 0

    @property
    def name(self):
        return self.__name

    def get_initial_response(self):
        state = AuthMechanism.CONTINUE if self.__challenges else AuthMechanism.OK
        return state, self.__initial_response

    def challenge_with(self, challenge):
        expected_challenge = self.__challenges[self.__challenge_pointer]
        if expected_challenge[0] != challenge:
            raise AssertionError('Wrong challenge: %s != %s' % (challenge, expected_challenge[0]))
        self.__challenge_pointer += 1
        status = AuthMechanism.CONTINUE if self.__challenge_pointer < len(self.__challenges) else AuthMechanism.OK
        return status, expected_challenge[1]


class AFakeAuthMechanism(object):
    NAME = 'SKEY'
    INITIAL_RESPONSE = None
    CHALLENGES = ()

    def __init__(self):
        self.__name = self.NAME
        self.__initial_response = self.INITIAL_RESPONSE
        self.__challenges = self.CHALLENGES

    def with_challenges(self, challenges):
        self.__challenges = challenges
        return self

    def with_any_challenge(self):
        self.__challenges = [('a', 'b')]
        return self

    def build(self):
        return FakeAuthMechanism(self.__name, self.__initial_response, self.__challenges)