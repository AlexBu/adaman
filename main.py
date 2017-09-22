#!/usr/bin/env python
# encoding: utf-8

import os
import sys
import struct
import clzs
import glob

class Archive():
    def __init__(self, name):
        self._file_info = dict(name = name, count = 0, entries = [])
        self._load_fl()
        self._load_fi()
        self._load_fs()

    def __str__(self):
        info = "archive info\n"
        info += self._get_name()
        info += self._get_entry()
        return info

    def _get_name(self):
        return "name: %s\n" % self._file_info['name']

    def _get_entry(self):
        total_str = 'entries \n'
        for entry in self._file_info['entries']:
            entry_str = 'entry name = %s,\tactual size = %d, encoded size = %d, offset = %x\n'\
                        % (entry['name'], entry['act_size'], entry['enc_size'], entry['offset'])
            total_str += entry_str
        return total_str

    def _load_fl(self):
        fl = open(self._file_info['name'] + '.fl', 'rb')
        for line in fl.readlines():
            self._file_info['entries'].append(dict(name = line.split('\\')[-1].rstrip()))
        self._file_info['count'] = len(self._file_info['entries'])

    def get_list(self):
        return [entry['name'] for entry in self._file_info['entries']]

    def get_index(self):
        return [entry['name'] for entry in self._file_info['entries']]

    def _load_fi(self):
        fi = open(self._file_info['name'] + '.fi', 'rb').read()
        print len(fi)
        for i in range(self._file_info['count']):
            (size, offset, lzs) = struct.unpack("<3I", fi[i*12 : (i + 1)*12])
            self._file_info['entries'][i]['act_size'] = size
            self._file_info['entries'][i]['offset'] = offset
            self._file_info['entries'][i]['lzsed'] = (lzs == 1)

    def _load_fs(self):
        previous = os.path.getsize(self._file_info['name'] + '.fs')
        for i in range(self._file_info['count'] - 1, -1, -1):
            self._file_info['entries'][i]['enc_size'] = previous - self._file_info['entries'][i]['offset']
            previous = self._file_info['entries'][i]['offset']

    def create_subfolder(self, name):
        if not os.path.exists(name):
            os.makedirs(name)

    def create_segments(self):
        self.create_subfolder(self._file_info['name'])

        fs = open(self._file_info['name'] + '.fs', 'rb')
        for entry in self._file_info['entries']:
            sub_name = './' + self._file_info['name'] + '/' + entry['name']
            tmp_name = sub_name + '.tmp'

            if entry['lzsed']:
                file_name_to_be_written = tmp_name
            else:
                if(entry['enc_size'] != entry['act_size']):
                    print entry
                assert (entry['enc_size'] == entry['act_size'])
                file_name_to_be_written = sub_name

            fs.seek(entry['offset'])
            enc_data = fs.read(entry['enc_size'])
            tmp = open(file_name_to_be_written, 'wb')
            tmp.write(enc_data)
            tmp.close()

            if entry['lzsed']:
                decode_result = clzs.decode_file(tmp_name, sub_name)
                assert (decode_result == 0)
                os.remove(tmp_name)

        fs.close()

class ArchiveFolder():
    def __init__(self, dir):
        self.archive_list = map(lambda one_file: os.path.splitext(os.path.basename(one_file))[0],  glob.glob(os.path.join(dir, '*.fs')))

    def __str__(self):
        return 'find %d archives in the folder %s\n' % (len(self.archive_list), self.archive_list)

    def unpack(self):
        for entry in self.archive_list:
            ar = Archive(entry)
            print ar
            ar.create_segments()

    def pack(self):
        pass


def __main():
    if len(sys.argv) != 3:
        print '--pack <folder>    pack up everything'
        print '--unpack <folder>  unpack and overwrite everything'
        return
    if sys.argv[1] == '--pack':
        pack = True
    elif sys.argv[1] == '--unpack':
        pack = False
    else:
        print '--pack <folder>    pack up everything'
        print '--unpack <folder>  unpack and overwrite everything'
        return
    af = ArchiveFolder(sys.argv[2])
    print af
    if pack:
        af.pack()
    else:
        af.unpack()
    print af


if __name__ == '__main__':
    __main()
