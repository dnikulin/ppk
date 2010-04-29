# Copyright (c) 2010 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

'''
Convenience classes for bit stream encoding/decoding.
'''

__all__ = ['BitReader', 'BitWriter', 'mask', 'read0', 'write0']


class BitReader(object):
    '''Bit stream reader.'''

    def __init__(self, getbyte):
        '''
        Create a bit stream reader with the given byte reader function.
        getbyte() must return a Python int 0<=b<=255, or raise EOFError.
        '''
        self.getbyte = getbyte
        self.skip()

    def skip(self):
        '''
        Skip the rest of the byte, if any, buffered from the reader function.
        The next read request will draw at least one byte from the reader function.
        '''
        self.byte = 0
        self.byte_bits = 8

    def __call__(self, bits):
        '''
        Read bits from the buffered byte (if any) and any further bytes (if necessary).
        '''
        assert bits > 0
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
                self.byte = int(self.getbyte())
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



class BitWriter(object):
    '''Bit stream writer.'''

    def __init__(self, putbyte):
        '''
        Create a bit stream writer with the given byte writer function.
        putbyte() must accept a Python int 0<=b<=255.
        '''
        self.putbyte = putbyte
        self.byte = 0
        self.byte_bits = 0

    def flush(self):
        '''
        Write the current byte, if any, to the byte writer function.
        The next bit write request will start a new byte.
        '''
        if self.byte_bits > 0:
            self.byte_bits = 0
            self.putbyte(self.byte)
        self.byte = 0

    def __call__(self, bits, value):
        '''
        Write bits to the stream, flushing bytes as necessary.
        '''
        assert bits > 0
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
                self.flush()


def mask(bits):
    '''Calculate an integer mask 'bits' wide'''
    return (1L << bits) - 1L

def read0(*_, **__):
    '''Byte reader mock that always returns 0.'''
    return 0

def write0(*_, **__):
    '''Byte writer mock that ignores all parameters.'''
    pass

def readSequence(seq):
    '''Construct a bit reader that draws bytes from an iterable object.'''
    return BitReader(seq.__iter__().next)

def writeList(out):
    '''Construct a bit writer that appends bytes to a list.'''
    return BitWriter(out.append)
