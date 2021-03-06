# coding: utf-8
from vonpit_dbus.auth_mechanism import AuthMechanism


class DbusClientConnection(object):

    def __init__(self, transport):
        super(DbusClientConnection, self).__init__()
        self.__transport = transport
        self.__mechanism = None
        self.__authenticated = False
        self.__unix_fd_passing_enabled = False

    def start(self):
        self.__transport.send_null_byte()

    def request_available_mechanisms(self):
        self.__transport.send_line('AUTH')
        response = self.__transport.recv_command()
        if not response.startswith('REJECTED '):
            raise DbusConnectionError
        return response.split()[1:]

    def authenticate_with(self, mechanism):
        self.__mechanism = mechanism
        self.__start_authentication()

    def __start_authentication(self):
        status, initial_response = self.__mechanism.get_initial_response()
        if initial_response:
            self.__transport.send_line('AUTH %s %s' % (self.__mechanism.name, initial_response))
        else:
            self.__transport.send_line('AUTH %s' % self.__mechanism.name)

        if status == AuthMechanism.CONTINUE:
            self.__wait_for_auth_data()
        else:
            self.__wait_for_auth_ok()

    def __wait_for_auth_data(self):
        server_command, _, parameters = self.__transport.recv_command().partition(' ')

        if server_command == 'DATA':
            self.__challenge_mechanism(parameters)
        elif server_command == 'REJECTED':
            raise DbusAuthenticationFailure
        elif server_command == 'ERROR':
            self.__transport.send_line('CANCEL')
            self.__wait_for_auth_reject()
        elif server_command == 'OK':
            self.__authenticated = True
        else:
            self.__transport.send_line('ERROR')
            self.__wait_for_auth_data()

    def __challenge_mechanism(self, challenge):
        status, response = self.__mechanism.challenge_with(challenge)
        self.__transport.send_line('DATA %s' % response)

        if status == AuthMechanism.CONTINUE:
            self.__wait_for_auth_data()
        else:
            self.__wait_for_auth_ok()

    def __wait_for_auth_reject(self):
        server_command, _, parameters = self.__transport.recv_command().partition(' ')
        if server_command == 'REJECTED':
            raise DbusAuthenticationFailure
        else:
            self.__transport.close()
            raise DbusConnectionError

    def __wait_for_auth_ok(self):
        server_command, _, parameters = self.__transport.recv_command().partition(' ')
        if server_command == 'OK':
            self.__authenticated = True
        elif server_command == 'REJECTED':
            raise DbusAuthenticationFailure
        elif server_command in ('DATA', 'ERROR'):
            self.__transport.send_line('CANCEL')
            self.__wait_for_auth_reject()
        else:
            self.__transport.send_line('ERROR')
            self.__wait_for_auth_ok()

    @property
    def authenticated(self):
        return self.__authenticated

    def negotiate_unix_fd(self):
        self.__transport.send_line('NEGOTIATE_UNIX_FD')
        response = self.__transport.recv_command()
        if response == 'AGREE_UNIX_FD':
            self.__unix_fd_passing_enabled = True
        elif response == 'ERROR':
            self.__unix_fd_passing_enabled = False
        else:
            raise DbusConnectionError

    @property
    def unix_fd_passing_enabled(self):
        return self.__unix_fd_passing_enabled

    def begin(self):
        self.__transport.send_line('BEGIN')


class DbusConnectionError(Exception):
    pass


class DbusAuthenticationFailure(DbusConnectionError):
    pass