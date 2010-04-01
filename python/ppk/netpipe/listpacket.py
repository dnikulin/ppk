#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE for details
# Part of the PPK project

from cStringIO import StringIO
import struct

COUNT_FMT = '!I'
COUNT = struct.Struct(COUNT_FMT)
COUNT_SIZE = struct.calcsize(COUNT_FMT)

CHAN_FMT = '!IIIQI' # readers, writers, objects, bytes, name length
CHAN = struct.Struct(CHAN_FMT)
CHAN_SIZE = struct.calcsize(CHAN_FMT)

def makeListPacket(channels):
    out = StringIO()

    out.write(COUNT.pack(len(channels)))

    for channel in channels:
        name = channel.name.encode('utf-8')

        # Swap readers and writers
        readers = len(channel.writers)
        writers = len(channel.readers)
        objects = channel.totalObjects
        bytes = channel.totalBytes

        out.write(CHAN.pack(readers, writers, objects, bytes, len(name)))
        out.write(name)

    return out.getvalue()

def readListPacket(packet):
    ins = StringIO(packet)

    count = COUNT.unpack(ins.read(COUNT_SIZE))[0]

    out = []
    for _ in range(count):
        parts = CHAN.unpack(ins.read(CHAN_SIZE))
        readers, writers, objects, bytes, namelen = parts

        name = ins.read(namelen).decode('utf-8')
        out.append((name, readers, writers, objects, bytes))

    return out
