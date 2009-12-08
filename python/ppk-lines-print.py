#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

import ppk

import sys

if __name__ == '__main__':
    if len(sys.argv) != 1:
        ppk.printUsage()

    for _, body in ppk.readRaw():
        print body
