from models import *
from exceptions import *

import unittest

class TestGlobalManager(unittest.TestCase):

    instance = None

    def setUp(self):
        self.instance = GlobalManager()

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