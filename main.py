#!/usr/bin/env python
# encoding: utf-8

import sys
from archivefolder import ArchiveFolder

def __main():
    if len(sys.argv) != 3:
        print('--pack <folder>    pack up everything')
        print('--unpack <folder>  unpack and overwrite everything')
        return
    if sys.argv[1] == '--pack':
        pack = True
    elif sys.argv[1] == '--unpack':
        pack = False
    else:
        print('--pack <folder>    pack up everything')
        print('--unpack <folder>  unpack and overwrite everything')
        return
    af = ArchiveFolder(sys.argv[2])
    if pack:
        af.pack()
    else:
        af.unpack()


if __name__ == '__main__':
    __main()
