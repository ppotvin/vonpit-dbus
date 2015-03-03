# coding: utf-8
import socket
import unittest

from vonpit_dbus.transports.socket import SocketClientTransport


@unittest.skipIf(not hasattr(socket, 'socketpair'), 'socketpair is unavailable')
class SocketClientTransportUnitTest(unittest.TestCase):
    def setUp(self):
        super(SocketClientTransportUnitTest, self).setUp()
        self.test_socket, self.transport_socket = socket.socketpair()

    def test_when_send_null_byte_should_send_null_byte(self):
        transport = SocketClientTransport(self.transport_socket)

        transport.send_null_byte()
        result = self.test_socket.recv(1024)

        self.assertEqual(result, b'\x00')

    def test_when_send_line_should_send_line(self):
        transport = SocketClientTransport(self.transport_socket)
        a_line = 'A' * 2048

        transport.send_line(a_line)
        result = self.__recv(len(a_line)+2)

        self.assertEquals(a_line + '\r\n', result.decode('utf-8'))

    def __recv(self, to_read):
        result = b''
        while to_read:
            data = self.test_socket.recv(4096)
            result += data
            to_read -= len(data)
        return result

    def test_when_close_should_close_socket(self):
        transport = SocketClientTransport(self.transport_socket)

        transport.close()
        result = self.test_socket.recv(1024)

        self.assertEquals(result, b'')

    def test_when_read_command_should_read_from_socket(self):
        transport = SocketClientTransport(self.transport_socket)
        a_command = 'HELLO YOU'
        data = '%s\r\nHOW ARE YOU?\r\n' % a_command
        self.test_socket.send(data.encode('ascii'))

        result = transport.recv_command()

        self.assertEquals(a_command, result)

    def test_when_read_two_commands_should_split_correctly(self):
        transport = SocketClientTransport(self.transport_socket)
        a_command = 'HELLO YOU'
        another_command = 'HOW ARE YOU?'
        data = '%s\r\n%s\r\n' % (a_command, another_command)
        self.test_socket.send(data.encode('ascii'))

        result1 = transport.recv_command()
        result2 = transport.recv_command()

        self.assertEquals(a_command, result1)
        self.assertEquals(another_command, result2)
