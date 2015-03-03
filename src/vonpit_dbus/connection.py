# coding: utf-8
from vonpit_dbus.auth_mechanism import AuthMechanism


class DbusConnection(object):

    def __init__(self, transport):
        super(DbusConnection, self).__init__()
        self.__transport = transport
        self.__mechanism = None
        self.__authenticated = False

    def start_client(self):
        self.__transport.send_null_byte()

    def get_available_mechanisms(self):
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

    def __wait_for_auth_ok(self):
        self.__transport.recv_command()

    @property
    def authenticated(self):
        return self.__authenticated


class DbusConnectionError(Exception):
    pass


class DbusAuthenticationFailure(DbusConnectionError):
    pass