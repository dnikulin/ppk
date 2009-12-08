#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

import ppk

import sys
import zlib

if __name__ == '__main__':
    if len(sys.argv) != 1:
        ppk.printUsage()

    for _, zbody in ppk.readRaw():
        body = zlib.decompress(zbody)

        ilen = len(zbody)
        olen = len(body)
        pcent = ppk.percent(olen, ilen)

        ppk.report("%d -> %d (%d%%)" % (ilen, olen, pcent))

        ppk.writeRaw(body)
