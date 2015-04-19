# coding: utf-8
from vonpit_dbus import DBUS_BIG_ENDIAN, DBUS_LITTLE_ENDIAN
from vonpit_dbus.types.string_like import String, Signature
from vonpit_dbus.types.tests import DbusBasicTypeUnitTest


class StringUnitTest(DbusBasicTypeUnitTest):

    type_under_test = String

    def test_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(u'hello', DBUS_BIG_ENDIAN, b'\x00\x00\x00\x05hello\x00')

    def test_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(u'hello', DBUS_LITTLE_ENDIAN, b'\x05\x00\x00\x00hello\x00')


class SignatureUnitTest(DbusBasicTypeUnitTest):

    type_under_test = Signature

    def test_big_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(u'i(ii)', DBUS_BIG_ENDIAN, b'\x05i(ii)\x00')

    def test_little_endian_when_pack_should_return_packed_value(self):
        self._test_when_pack_should_return_packed_value(u'i(ii)', DBUS_LITTLE_ENDIAN, b'\x05i(ii)\x00')
