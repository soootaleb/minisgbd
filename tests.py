from models import *
from exceptions import *

import unittest

class TestGlobalManager(unittest.TestCase):

    instance = None

    def setUp(self):
        self.instance = GlobalManager()

    def test_calculate_slot_count(self):
        self.assertEqual(0, self.instance.calculate_slot_count(10, 10))
        self.assertEqual(1, self.instance.calculate_slot_count(10, 11))
        self.assertEqual(1, self.instance.calculate_slot_count(10, 21))
        self.assertEqual(2, self.instance.calculate_slot_count(10, 22))
        self.assertEqual(9, self.instance.calculate_slot_count(100, 1000))


    def test_calculate_record_size(self):
        self.assertEqual(4, self.instance.calculate_record_size(['int']))
        self.assertEqual(4, self.instance.calculate_record_size(['float']))
        self.assertEqual(10, self.instance.calculate_record_size(['string10']))
        self.assertEqual(40, self.instance.calculate_record_size(['string40']))

        self.assertEqual(16, self.instance.calculate_record_size([
            'int', 'int', 'float', 'string1', 'string3'
        ]))

        with self.assertRaises(MiniColumnTypeError):
            self.instance.calculate_record_size(['into'])
        with self.assertRaises(MiniColumnTypeError):
            self.instance.calculate_record_size(['string'])
        with self.assertRaises(MiniColumnTypeError):
            self.instance.calculate_record_size(['stringA'])


if __name__ == '__main__':
    unittest.main()