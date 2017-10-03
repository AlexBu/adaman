#!/usr/bin/env python
# encoding: utf-8

import struct
import clzs
import os

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
            entry_str = 'entry name = %s,\tactual size = %d, encoded size = %d, offset = %x\n' \
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
        print(len(fi))
        for i in range(self._file_info['count']):
            (size, offset, lzs) = struct.unpack("<3I", fi[i*12 : (i + 1)*12])
            self._file_info['entries'][i]['act_size'] = size
            self._file_info['entries'][i]['offset'] = offset
            self._file_info['entries'][i]['lzsed'] = (lzs == 1)

    def _load_fs(self):
        previous = os.path.getsize(self._file_info['name'] + '.fs')
        for i in range(self._file_info['count'] - 1, -1, -1):
            if self._file_info['entries'][i]['lzsed']:
                self._file_info['entries'][i]['enc_size'] = previous - self._file_info['entries'][i]['offset']
            else:
                self._file_info['entries'][i]['enc_size'] = self._file_info['entries'][i]['act_size']
            previous = self._file_info['entries'][i]['offset']

    def create_subfolder(self, name):
        if not os.path.exists(name):
            os.makedirs(name)

    def create_segments(self):
        self.create_subfolder(self._file_info['name'])

        fs = open(self._file_info['name'] + '.fs', 'rb')
        for entry in self._file_info['entries']:
            sub_name = self._file_info['name'] + '/' + entry['name']
            tmp_name = sub_name + '.tmp'
            print('extracting %s' % sub_name)

            if entry['lzsed']:
                file_name_to_be_written = tmp_name
            else:
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


