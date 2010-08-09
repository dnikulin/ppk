# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

'''
Convenience classes for packet encoding/decoding.
'''

import struct
from cStringIO import StringIO

from bitio import BitReader, BitWriter
from errors import FormatError

__all__ = ["Reader", "Writer"]

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
        self.bitter = BitReader(self.readByte)

    def read(self, size):
        '''
        read(size) -> string
        Read bytes into a raw string.
        '''
        return self.stream.read(size)

    def readStruct(self, format):
        '''
        readStruct(format) -> tuple
        Read a structure from the stream.
        Raises FormatError() if bytes were unavailable.
        '''
        size = struct.calcsize(format)
        bytes = self.read(size)
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
        bytes = self.read(size)
        if len(bytes) != size:
            raise FormatError()
        return bytes.decode("utf-8")

    def readByte(self):
        '''
        readByte() -> int
        Read a single byte.
        '''
        return ord(self.read(1))

    def readBits(self, bits):
        '''
        Read bits (see ppk.bitio.BitReader).
        '''
        return self.bitter(bits)

    def skipBits(self):
        '''
        Skip buffered bits (see ppk.bitio.BitReader).
        '''
        self.bitter.skip()



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
        self.bitter = BitWriter(self.writeByte)

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

    def writeByte(self, value):
        '''
        Write a single byte.
        '''
        self.stream.write(chr(value))

    def writeBits(self, bits, value):
        '''
        Write a series of bits (see ppk.bitio.BitWriter).
        '''
        self.bitter(bits, value)

    def flushBits(self):
        '''
        Flush buffered bits, if any (see ppk.bitio.BitWriter).
        '''
        self.bitter.flush()

    def finish(self):
        '''
        finish() -> contents
        Retrieve stream contents if backed by StringIO.
        '''
        self.flushBits()
        return self.stream.getvalue()
