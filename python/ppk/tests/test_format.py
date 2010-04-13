# -*- coding: utf-8 -*-

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

import unittest

from ppk import Reader, Writer

class FormatTest(unittest.TestCase):
    def testStruct(self):
        fmt = '!IBi'
        values = (8, 97, -12)

        out = Writer()
        out.writeStruct(fmt, *values)

        pack = out.finish()
        ipack = Reader(pack)

        nvalues = ipack.readStruct(fmt)
        self.assertEquals(values, nvalues)

        left = ipack.stream.read()
        self.assertFalse(left)

    def testString(self):
        strings = ['', '01823', 'ascii', 'юникод']

        out = Writer()
        for string in strings:
            out.writeString(string)

        pack = out.finish()
        ipack = Reader(pack)

        for string in strings:
            nstring = ipack.readString()
            self.assertEqual(string, nstring)

        left = ipack.stream.read()
        self.assertFalse(left)

    def testBits(self):
        MASK32 = 0xFFFFFFFF
        MASK64 = (MASK32 << 32) | MASK32

        values = [
            (9, 312),
            (1, 0),
            (1, 1),
            (32, 0),
            (64, 0),
            (32, MASK32),
            (64, MASK64),
        ]

        out = Writer()
        for bits, value in values:
            self.assertTrue(value >= 0)
            self.assertTrue(value <= MASK64)
            out.writeBits(bits, value)

        pack = out.finish()
        ipack = Reader(pack)

        for bits, value in values:
            nvalue = ipack.readBits(bits)
            self.assertEquals(value, nvalue)

        left = ipack.stream.read()
        self.assertFalse(left)

if __name__ == "__main__":
    unittest.main()
