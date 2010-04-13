# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

'''
Convenience classes for packet encoding/decoding.
'''

import struct
from cStringIO import StringIO

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

    def readStruct(self, format):
        '''
        readStruct(format) -> tuple
        Read a structure from the stream.
        Raises FormatError() if bytes were unavailable.
        '''
        size = struct.calcsize(format)
        bytes = self.stream.read(size)
        if len(bytes) < size:
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
        if len(bytes) < size:
            raise FormatError()
        return bytes.decode("utf-8")

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

    def writeStruct(self, format, *items):
        '''
        Write a structure.
        '''
        bytes = struct.pack(format, *items)
        self.stream.write(bytes)

    def writeString(self, string):
        '''
        Write a UTF8-encoded string.
        '''
        bytes = string.encode("utf-8")
        self.writeStruct("!I", len(bytes))
        self.stream.write(bytes)

    def finish(self):
        '''
        finish() -> contents
        Retrieve stream contents if backed by StringIO.
        '''
        return self.stream.getvalue()
