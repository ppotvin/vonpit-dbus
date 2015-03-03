# coding:utf-8
import six

from vonpit_dbus.transports import DbusClientTransport


class SocketClientTransport(DbusClientTransport):
    BUFFER_SIZE = 2048

    def __init__(self, socket):
        self.__socket = socket
        self.__buffer = bytearray(self.BUFFER_SIZE)
        self.__size_used_in_buffer = 0

    def recv_command(self):
        self.__recv_until_end_of_line()
        command = self.__get_line_and_replace_buffer()

        return command.decode('ascii')

    def __recv_until_end_of_line(self):
        available_buffer = memoryview(self.__buffer)[self.__size_used_in_buffer:]
        while len(available_buffer):
            if b'\r\n' in self.__buffer[:self.__size_used_in_buffer]:
                break
            received_size = self.__socket.recv_into(available_buffer)
            self.__size_used_in_buffer += received_size
            available_buffer = available_buffer[received_size:]

        if b'\r\n' not in self.__get_received_data():
            raise IOError('Buffer overrun')

    def __get_line_and_replace_buffer(self):
        line, _, rest_of_data = self.__buffer[:self.__size_used_in_buffer].partition(b'\r\n')
        self.__replace_buffer_with(rest_of_data)
        return line

    def __replace_buffer_with(self, data):
        self.__buffer = bytearray(self.BUFFER_SIZE)
        self.__buffer[:len(data)] = data
        self.__size_used_in_buffer = len(data)

    def __get_received_data(self):
        return self.__buffer[:self.__size_used_in_buffer]

    def send_line(self, line):
        if isinstance(line, six.text_type):
            line = line.encode('ascii')
        self.__socket.sendall(line + b'\r\n')

    def close(self):
        self.__socket.close()

    def send_null_byte(self):
        self.__socket.send(b'\x00')
