# coding: utf-8

import unittest

from vonpit_dbus.types import DbusBasicType


class DbusBasicTypeUnitTest(unittest.TestCase):

    type_under_test = DbusBasicType

    def _test_when_pack_should_return_packed_value(self, value, endianness, expected_result):
        result = self.type_under_test.pack(value, endianness)
        self.assertEquals(result, expected_result)
