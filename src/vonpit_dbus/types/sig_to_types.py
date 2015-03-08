# coding: utf-8
import six
from vonpit_dbus.types.fixed import Byte, Boolean, Int16, Uint16, Int32, Uint32, Int64, Uint64, Double, UnixFd
from vonpit_dbus.types.string_like import String


class SignatureToTypesConverter(object):
    BASIC_TYPES = (
        Byte,
        Boolean,
        Int16,
        Uint16,
        Int32,
        Uint32,
        Int64,
        Uint64,
        Double,
        UnixFd,
        String,
    )

    def __init__(self):
        self.__codes = {
            dbus_type.CODE: dbus_type for dbus_type in self.BASIC_TYPES
        }

    def convert(self, signature):
        types = []
        if isinstance(signature, six.text_type):
            signature = signature.encode('utf-8')
        remaining_signature = memoryview(signature)
        while True:
            next_type, remaining_signature = self.__read_next_type(remaining_signature)
            types.append(next_type)
            if not remaining_signature:
                break
        return tuple(types)

    def __read_next_type(self, remaining_signature):
        code = chr(remaining_signature[0])
        if code in self.__codes:
            return self.__codes[code](), remaining_signature[1:]
        else:
            print(code)
            raise ValueError
