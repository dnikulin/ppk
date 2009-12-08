#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

import ppk

import sys
import zlib

if __name__ == '__main__':
    if len(sys.argv) > 2:
        ppk.printUsage("[level = 9]")

    level = 9

    if len(sys.argv) > 1:
        level = int(sys.argv[1])

    for _, body in ppk.readRaw():
        zbody = zlib.compress(body, level)
        
        ilen = len(body)
        olen = len(zbody)
        pcent = ppk.percent(olen, ilen)

        ppk.report("%d -> %d (%d%%)" % (ilen, olen, pcent))

        ppk.writeRaw(zbody)
