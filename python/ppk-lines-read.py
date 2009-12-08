#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

import ppk

import sys

if __name__ == '__main__':
    sys.stdin.close()

    if len(sys.argv) < 2:
        ppk.printUsage("<file0> [... fileN]")

    for path in sys.argv[1:]:
        with open(path, 'rt') as fd:
            for line in fd:
                ppk.writeRaw(line.rstrip())
