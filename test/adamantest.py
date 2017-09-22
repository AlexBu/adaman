#!/usr/bin/env python
# encoding: utf-8

import unittest
import main
import filecmp


class ArchiveTest(unittest.TestCase):

    def setUp(self):
        self.name_list = ['1.lzs', '2.lzs', '3.lzs', 'Credits.tim', 'discerr.lzs', 'discimg1.lzs', 'discimg2.lzs', 'discimg3.lzs', 'discimg4.lzs', 'harata.cnf', 'icon.tim', 'init.out', 'kernel.bin', 'namedic.bin', 'sysfnt.tdw', 'wm2field.tbl', 'ff8.lzs', 'loop01.lzs', 'loop02.lzs', 'loop03.lzs', 'loop04.lzs', 'loop05.lzs', 'loop06.lzs', 'loop07.lzs', 'loop08.lzs', 'loop09.lzs', 'loop10.lzs', 'loop11.lzs', 'loop12.lzs', 'loop13.lzs', 'loop14.lzs', 'name01.lzs', 'name02.lzs', 'name03.lzs', 'name04.lzs', 'name05.lzs', 'name06.lzs', 'name07.lzs', 'name08.lzs', 'name09.lzs', 'name10.lzs', 'name11.lzs', 'name12.lzs', 'name13.lzs', 'name14.lzs', 'square.lzs' ]
        self.ar = main.Archive('../testdata/main')

    def tearDown(self):
        pass

    def test_list_loading(self):
        new_list = self.ar.get_list()
        self.assertEquals(new_list, self.name_list)

    @unittest.skip("not to touch files and folders")
    def test_data_loadin(self):
        self.ar.create_segments()
        compare_result = filecmp.dircmp('./main', './expected/main')
        self.assertEquals(len(compare_result.diff_files), 0)

class ArchiveFolderTest(unittest.TestCase):
    def setUp(self):
        self.af = main.ArchiveFolder('../testdata')

    def tearDown(self):
        pass

    def test_find_archive(self):
        print self.af

    def test_extract_archives(self):
        self.af.unpack()

    def test_pack_archives(self):
        self.af.pack()

if __name__ == '__main__':
    unittest.main()