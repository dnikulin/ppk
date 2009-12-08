#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

import ppk

import os
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        ppk.printUsage("<directory>")

    for head, body in ppk.readRaw():
        hash = ppk.hashBodyHex(body)

        path = os.path.join(sys.argv[1], hash)

        try:
            with open(path, 'wb') as fd:
                fd.write(body)

            sys.stdout.write(head)
            sys.stdout.write(body)

            ppk.report("wrote %s (%lu bytes)" % (hash, len(body)))
        except ex:
            ppk.report("could not write %s: %s" % (hash, str(ex)))
