from models import *
from helpers import *
from exceptions import *

import unittest, os

class TestDiskManager(unittest.TestCase):

    instance = None

    def setUp(self):
        self.instance = DiskManager()

    def tearDown(self):
        for f in os.listdir(DATABASE):
            os.remove(os.path.join(DATABASE, f))

    def test_create_file(self):
        file_id = 1337
        filename = mount_file_name(file_id)
        filepath = os.path.join(DATABASE, filename)
        self.instance.create_file(file_id)
        self.assertTrue(os.path.isfile(filepath))
        self.assertRaises(MiniFileExistsError, self.instance.create_file, file_id)
        self.assertRaises(MiniFileNameValueError, self.instance.create_file, None)
        self.assertRaises(MiniFileNameValueError, self.instance.create_file, 'str')
        self.assertRaises(MiniFileNameValueError, self.instance.create_file, -1)

    def print(self):
        f = open('db/Data_1337.rf', 'rb')
        f.seek(0)
        print(f.read())
        f.close()

    def test_add_page(self):
        '''
            With n strings of m chars added to file, it should append a new page at the index

            3(n - 1) + n*m

            Its a byte per character, and we add DATA_SET (3 characters between each word)
        '''
        file_id = 1337
        filename = mount_file_name(file_id)
        filepath = os.path.join(DATABASE, filename)
        self.instance.create_file(file_id)

        pid1 = self.instance.add_page(file_id)
        self.assertEqual(0, pid1.idx)
        self.assertEqual(file_id, pid1.file_id)

        # Writing on first page to add content & test page 2
        self.instance.write_page(pid1, ['Hello', 'World', '!'])

        pid2 = self.instance.add_page(file_id)
        self.assertEqual(17, pid2.idx)
        self.assertEqual(file_id, pid2.file_id)

    def test_write_page(self):
        '''
            We are adding pages for different tests in order to avoid previous test leftovers.
            e.g if we write over a bigger string, the end of the bigger one will still be append to the lastly added one
        '''
        file_id = 1337
        filename = mount_file_name(file_id)
        filepath = os.path.join(DATABASE, filename)
        self.instance.create_file(file_id)

        pid1 = self.instance.add_page(file_id)
        page1 = ['Hello', 'World']
        self.instance.write_page(pid1, page1)

        pid2 = self.instance.add_page(file_id)
        page2 = ['Bye', '', 'bye', None, 'world']
        self.instance.write_page(pid2, page2)
        
        file = open('db/Data_1337.rf', 'rb')
        file.seek(pid1.idx)
        content1 = file.read(pid2.idx - pid1.idx) # Just read the first page
        file.seek(pid2.idx)
        content2 = file.read()

        expected1 = bytes(DATA_SEP.join([o if o is not None else '' for o in page1]), encoding='utf-8')
        expected2 = bytes(DATA_SEP.join([o if o is not None else '' for o in page2]), encoding='utf-8')

        self.assertEqual(content1, expected1)
        self.assertEqual(content2, expected2)

        file.close()

    def test_read_page(self):
        '''
            We are adding pages for different tests in order to avoid previous test leftovers.
            e.g if we write over a bigger string, the end of the bigger one will still be append to the lastly added one

            FIXME: This test is not passing because we used to fix PAGE_SIZE to 4096 bytes
            but we ended with variable pages at writing (write_page)
        '''
        file_id = 1337
        filename = mount_file_name(file_id)
        filepath = os.path.join(DATABASE, filename)
        self.instance.create_file(file_id)

        pid1 = self.instance.add_page(file_id)
        content1 = ['Hello', 'World']
        self.instance.write_page(pid1, content1)

        pid2 = self.instance.add_page(file_id)
        content2 = ['Bye', '', 'bye', None, 'world']
        self.instance.write_page(pid2, content2)

        buffer1 = []
        buffer2 = []
            
        self.instance.read_page(pid1, buffer1)
        self.instance.read_page(pid2, buffer2)

        self.assertEqual(content1, buffer1)
        self.assertEqual(content2, buffer2)

        file.close()
        

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