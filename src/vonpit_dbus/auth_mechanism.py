# coding: utf-8
import abc


class AuthMechanism(object):
    CONTINUE = object()
    OK = object()
    ERROR = object()

    @abc.abstractproperty
    def name(self):
        return 'ABSTRACT_MECHANISM'

    def get_initial_response(self):
        return self.CONTINUE, None

    @abc.abstractmethod
    def challenge_with(self, challenge):
        return self.ERROR, None

    @classmethod
    def __subclasshook__(cls, subclass):
        required_methods = ['name', 'get_initial_response', 'challenge_with']
        if cls is AuthMechanism:
            for method in required_methods:
                if not any(method in B.__dict__ for B in subclass.__mro__):
                    return False
            return True
        return NotImplemented