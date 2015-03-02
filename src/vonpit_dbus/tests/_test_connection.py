# coding: utf-8
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
