# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

'''
Convenience classes for packet encoding/decoding.
'''

import struct
from cStringIO import StringIO

from errors import FormatError

__all__ = ["Reader", "Writer", "mask"]

def mask(bits):
    return (1L << bits) - 1L

class Reader(object):
    '''
    Structure stream reader.
    '''

    def __init__(self, string = None, file = None):
        '''
        Wrap a string or file stream in a structure reader.
        Either string or file must be given.
        '''
        if string is not None:
            self.stream = StringIO(string)
        elif file is not None:
            self.stream = file
        else:
            raise "string or file must be non-None"

        # Bit reader buffer
        self.byte = 0
        self.byte_bits = 8

    def readStruct(self, format):
        '''
        readStruct(format) -> tuple
        Read a structure from the stream.
        Raises FormatError() if bytes were unavailable.
        '''
        size = struct.calcsize(format)
        bytes = self.stream.read(size)
        if len(bytes) != size:
            raise FormatError()
        return struct.unpack(format, bytes)

    def readString(self):
        '''
        readString() -> string
        Read a UTF8-encoded string from the stream.
        Raises FormatError() if bytes were unavailable.
        '''
        size = self.readStruct("!I")[0]
        bytes = self.stream.read(size)
        if len(bytes) != size:
            raise FormatError()
        return bytes.decode("utf-8")

    def readBits(self, bits):
        assert bits > 0
        assert bits <= 64
        assert self.byte_bits >= 0
        assert self.byte_bits <= 8

        out = 0
        done = 0

        while done < bits:
            assert self.byte_bits >= 0
            assert self.byte_bits <= 8

            more = min(8 - self.byte_bits, bits - done)
            assert more >= 0
            assert more <= 8

            if more < 1:
                self.byte = ord(self.stream.read(1))
                assert self.byte >= 0
                assert self.byte <= 0xFF
                self.byte_bits = 0
                continue

            value = self.byte >> self.byte_bits
            value &= mask(more)
            assert value >= 0
            assert value <= 0xFF

            value <<= done
            out |= value

            done += more
            assert done <= bits

            self.byte_bits += more
            assert self.byte_bits >= 0
            assert self.byte_bits <= 8

        assert (out & mask(bits)) == out
        return out

    def skipBits(self):
        self.byte = 0
        self.byte_bits = 8



class Writer(object):
    '''
    Structure stream writer.
    '''

    def __init__(self, stream = None):
        '''
        Wrap a stream with a structure writer.
        An internal StringIO stream is created if none is given.
        In this case, call finish() to retrieve the stream's contents.
        '''
        if stream is None:
            self.stream = StringIO()
        else:
            self.stream = stream

        # Bit writer buffer
        self.byte = 0
        self.byte_bits = 0

    def writeStruct(self, format, *items):
        '''
        Write a structure.
        '''
        self.flushBits()
        bytes = struct.pack(format, *items)
        self.stream.write(bytes)

    def writeString(self, string):
        '''
        Write a UTF8-encoded string.
        '''
        self.flushBits()
        bytes = string.encode("utf-8")
        self.writeStruct("!I", len(bytes))
        self.stream.write(bytes)

    def finish(self):
        '''
        finish() -> contents
        Retrieve stream contents if backed by StringIO.
        '''
        self.flushBits()
        return self.stream.getvalue()

    def writeBits(self, bits, value):
        assert bits > 0
        assert bits <= 64
        assert self.byte_bits >= 0
        assert self.byte_bits <= 8

        assert (value & mask(bits)) == value

        done = 0

        while done < bits:
            assert self.byte_bits >= 0
            assert self.byte_bits <= 8

            more = min(8 - self.byte_bits, bits - done)
            assert more > 0
            assert more <= 8

            downvalue = value >> done
            assert downvalue <= value
            assert (downvalue & mask(bits)) == downvalue

            byte = downvalue & mask(more)
            shifted = byte << self.byte_bits
            assert shifted >= byte
            assert (byte == 0) == (shifted == 0)

            self.byte |= shifted

            done += more
            assert done <= bits

            self.byte_bits += more
            assert self.byte_bits >= 0
            assert self.byte_bits <= 8

            if self.byte_bits >= 8:
                self.flushBits()

    def flushBits(self):
        if self.byte_bits > 0:
            self.stream.write(chr(self.byte))
            self.byte = 0
            self.byte_bits = 0

