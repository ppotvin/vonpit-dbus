# coding: utf-8
import unittest
from vonpit_dbus.types.container import Struct

from vonpit_dbus.types.fixed import Byte, Boolean, Int16, Uint16, Int32, Uint32, Int64, Uint64, Double, UnixFd
from vonpit_dbus.types.sig_to_types import SignatureToTypesConverter
from vonpit_dbus.types.string_like import String, ObjectPath, Signature


class SignatureToTypesConverterUnitTest(unittest.TestCase):
    def _test_when_convert_should_recognize_type(self, code, dbus_type):
        converter = SignatureToTypesConverter()
        result = converter.convert(code)

        self.assertEquals(len(result), 1)
        self.assertIsInstance(result[0], dbus_type)

    def test_unrecognized_type_when_convert_should_raise_ValueError(self):
        an_unknown_type = '*'
        converter = SignatureToTypesConverter()

        with self.assertRaises(ValueError):

            converter.convert(an_unknown_type)

    def test_byte_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('y', Byte)

    def test_boolean_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('b', Boolean)

    def test_int16_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('n', Int16)

    def test_uint16_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('q', Uint16)

    def test_int32_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('i', Int32)

    def test_uint32_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('u', Uint32)

    def test_int64_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('x', Int64)

    def test_uint64_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('t', Uint64)

    def test_double_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('d', Double)

    def test_unix_fd_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('h', UnixFd)

    def test_string_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('s', String)

    def test_object_path_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('o', ObjectPath)

    def test_signature_when_convert_should_recognize_type(self):
        self._test_when_convert_should_recognize_type('g', Signature)

    def test_two_fixed_type_codes_when_convert_should_return_two_tuple(self):
        signature = 'ui'
        types = (Uint32, Int32)
        converter = SignatureToTypesConverter()

        result = converter.convert(signature)

        self.assertEqual(len(result), len(types))
        for result_type, expected_type in zip(result, types):
            self.assertIsInstance(result_type, expected_type)

    def test_struct_of_two_integers_when_convert_should_return_struct_of_two_integers(self):
        signature = '(iu)'
        converter = SignatureToTypesConverter()

        result = converter.convert(signature)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Struct)
        enclosed_types = result[0].enclosed_types
        self.assertEqual(len(enclosed_types), 2)
        self.assertIsInstance(enclosed_types[0], Int32)
        self.assertIsInstance(enclosed_types[1], Uint32)

    def test_struct_inside_struct_when_convert_should_return_all_types(self):
        signature = '(i(ii))'
        converter = SignatureToTypesConverter()

        result = converter.convert(signature)

        self.assertEqual(len(result), 1)
        self.assertIsInstance(result[0], Struct)
        enclosed_types = result[0].enclosed_types
        self.assertEqual(len(enclosed_types), 2)
        self.assertIsInstance(enclosed_types[0], Int32)
        self.assertIsInstance(enclosed_types[1], Struct)
        enclosed_types_level2 = enclosed_types[1].enclosed_types
        self.assertEqual(len(enclosed_types_level2), 2)
        self.assertIsInstance(enclosed_types_level2[0], Int32)
        self.assertIsInstance(enclosed_types_level2[1], Int32)
