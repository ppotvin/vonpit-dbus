# coding: utf-8
from vonpit_dbus import DBUS_LITTLE_ENDIAN, DBUS_BIG_ENDIAN
from vonpit_dbus.types.fixed import Byte, Int16, Uint16, Int32, Uint32, Int64, Uint64, Double
from vonpit_dbus.types.tests import DbusBasicTypeUnitTest


class ByteUnitTest(DbusBasicTypeUnitTest):

    type_under_test = Byte

    def test_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(12, DBUS_LITTLE_ENDIAN, b'\x0C')

    def test_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(12, DBUS_BIG_ENDIAN, b'\x0C')


class BooleanUnitTest(DbusBasicTypeUnitTest):

    type_under_test = Byte

    def test_false_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(False, DBUS_LITTLE_ENDIAN, b'\x00')

    def test_false_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(False, DBUS_BIG_ENDIAN, b'\x00')

    def test_true_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(True, DBUS_LITTLE_ENDIAN, b'\x01')

    def test_true_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(True, DBUS_BIG_ENDIAN, b'\x01')


class Int16UnitTest(DbusBasicTypeUnitTest):

    type_under_test = Int16

    def test_positive_number_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(13, DBUS_LITTLE_ENDIAN, b'\x0D\x00')

    def test_positive_number_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(13, DBUS_BIG_ENDIAN, b'\x00\x0D')

    def test_negative_number_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(-13, DBUS_LITTLE_ENDIAN, b'\xf3\xff')

    def test_negative_number_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(-13, DBUS_BIG_ENDIAN, b'\xff\xf3')


class Uint16UnitTest(DbusBasicTypeUnitTest):

    type_under_test = Uint16

    def test_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(65523, DBUS_LITTLE_ENDIAN, b'\xf3\xff')

    def test_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(65523, DBUS_BIG_ENDIAN, b'\xff\xf3')


class Int32UnitTest(DbusBasicTypeUnitTest):

    type_under_test = Int32

    def test_positive_number_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(15, DBUS_LITTLE_ENDIAN, b'\x0F\x00\x00\x00')

    def test_positive_number_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(15, DBUS_BIG_ENDIAN, b'\x00\x00\x00\x0F')

    def test_negative_number_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(-15, DBUS_LITTLE_ENDIAN, b'\xf1\xff\xff\xff')

    def test_negative_number_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(-15, DBUS_BIG_ENDIAN, b'\xff\xff\xff\xf1')


class Uint32UnitTest(DbusBasicTypeUnitTest):

    type_under_test = Uint32

    def test_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(4294967281, DBUS_LITTLE_ENDIAN, b'\xf1\xff\xff\xff')

    def test_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(4294967281, DBUS_BIG_ENDIAN, b'\xff\xff\xff\xf1')


class Int64UnitTest(DbusBasicTypeUnitTest):

    type_under_test = Int64

    def test_positive_number_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(16, DBUS_LITTLE_ENDIAN, b'\x10\x00\x00\x00\x00\x00\x00\x00')

    def test_positive_number_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(16, DBUS_BIG_ENDIAN, b'\x00\x00\x00\x00\x00\x00\x00\x10')

    def test_negative_number_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(-16, DBUS_LITTLE_ENDIAN, b'\xf0\xff\xff\xff\xff\xff\xff\xff')

    def test_negative_number_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(-16, DBUS_BIG_ENDIAN, b'\xff\xff\xff\xff\xff\xff\xff\xf0')


class Uint64UnitTest(DbusBasicTypeUnitTest):

    type_under_test = Uint64

    def test_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(
            2 ** 64 - 16,
            DBUS_LITTLE_ENDIAN,
            b'\xf0\xff\xff\xff\xff\xff\xff\xff',
        )

    def test_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(
            2 ** 64 - 16,
            DBUS_BIG_ENDIAN,
            b'\xff\xff\xff\xff\xff\xff\xff\xf0',
        )


class DoubleUnitTest(DbusBasicTypeUnitTest):

    type_under_test = Double

    def test_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(
            3.141592,
            DBUS_LITTLE_ENDIAN,
            b'\x7a\x00\x8b\xfc\xfa\x21\x09\x40'
        )


    def test_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(3.141592, DBUS_BIG_ENDIAN, b'\x40\x09\x21\xFA\xFC\x8B\x00\x7A')
