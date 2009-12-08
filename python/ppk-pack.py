#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

import ppk

import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        ppk.printUsage("<count | size<k|m|g> >")

    K = 1024
    FACTORS = {'k': K, 'm': K*K, 'g': K*K*K}

    request = sys.argv[1]
    unit = request[-1]

    count = 0
    size = 0

    if unit in FACTORS:
        size = int(request[:-1]) * FACTORS[unit]
    else:
        count = int(request)

    out = ""
    total = 0

    def release():
        global out
        global total

        if total > 0:
            ppk.report("packed %d objects into %d bytes" % (total, len(out)))

            ppk.writeRaw(out)
            out = ""
            total = 0

    for head, body in ppk.readRaw():
        out += head
        out += body
        total += 1

        if (((count > 0) and (total >= count)) or
            ((size > 0)  and (len(out) >= size))):

            release()

    release()
