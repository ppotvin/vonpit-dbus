# coding: utf-8
import six

from vonpit_dbus.types.container import Struct, Array, Variant, DictEntry
from vonpit_dbus.types.fixed import Byte, Boolean, Int16, Uint16, Int32, Uint32, Int64, Uint64, Double, UnixFd
from vonpit_dbus.types.string_like import String, ObjectPath, Signature


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
        ObjectPath,
        Signature,
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
        code = self.__get_next_letter(remaining_signature)
        if code in self.__codes:
            return self.__codes[code](), remaining_signature[1:]
        elif code == '(':
            return self.__read_struct(remaining_signature)
        elif code == ')':
            raise _StructEnding
        elif code == 'a':
            return self.__read_array(remaining_signature)
        elif code == 'v':
            return Variant(), remaining_signature[1:]
        elif code == '{':
            return self.__read_dict_entry(remaining_signature)
        elif code == '}':
            raise _DictEntryEnding
        else:
            raise ValueError

    @staticmethod
    def __get_next_letter(array):
        if isinstance(array[0], int):
            return chr(array[0])
        else:
            return array[0]

    def __read_struct(self, remaining_signature):
        types = []
        remaining_signature = remaining_signature[1:]
        while True:
            try:
                next_type, remaining_signature = self.__read_next_type(remaining_signature)
            except _StructEnding:
                break
            except IndexError:
                raise ValueError('STRUCT was not terminated correctly. Missing ")" character')
            types.append(next_type)
        return Struct(types), remaining_signature[1:]

    def __read_array(self, remaining_signature):
        enclosed_type, remaining_signature = self.__read_next_type(remaining_signature[1:])
        return Array(enclosed_type), remaining_signature

    def __read_dict_entry(self, remaining_signature):
        types = []
        remaining_signature = remaining_signature[1:]
        while True:
            try:
                next_type, remaining_signature = self.__read_next_type(remaining_signature)
            except _DictEntryEnding:
                break
            except IndexError:
                raise ValueError('DICT_ENTRY was not terminated correctly. Missing "}" character')
            types.append(next_type)
        if len(types) != 2:
            raise ValueError('Wrong number of fields in DICT_ENTRY definition. Got %d instead' % len(types))
        return DictEntry(*types), remaining_signature[1:]


class _StructEnding(ValueError):
    pass


class _DictEntryEnding(ValueError):
    pass
