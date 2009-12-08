#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

import ppk

import os
import sys

if __name__ == '__main__':
    if len(sys.argv) < 2:
        ppk.printUsage("<directory> [hashes ...]")

    sys.stdin.close()

    root = sys.argv[1]
    for hash in sys.argv[2:]:
        path = os.path.join(root, hash)

        body = ""

        try:
            with open(path, 'rb') as fd:
                body = fd.read()
    
            nhash = ppk.hashBodyHex(body)

            if hash == nhash:
                ppk.report("read %s (%lu bytes)" % (hash, len(body)))
                ppk.writeRaw(body)
            else:
                ppk.report("read %s but hashed as %s (%lu bytes)"
                          % (hash, nhash, len(body)))
        except IOError, er:
            ppk.report(str(er))
