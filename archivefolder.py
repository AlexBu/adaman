#!/usr/bin/env python
# encoding: utf-8

from archive import Archive
import os
import glob

class ArchiveFolder():
    def __init__(self, dir):
        self.archive_dir = os.path.abspath(dir)
        self.archive_list = map(lambda one_file: os.path.splitext(os.path.basename(one_file))[0],  glob.glob(os.path.join(self.archive_dir, '*.fi')))

    def __str__(self):
        return 'find %d archives in the folder %s\n' % (len(self.archive_list), self.archive_list)

    def unpack(self):
        # search archives, unpack all available files
        for entry in self.archive_list:
            ar = Archive(os.path.join(self.archive_dir, entry))
            print(ar)
            ar.create_segments()

    def pack(self):
        # search archives and their folders, pack all available files
        # do not change the attribute of the current entry(packed or not)
        pass

