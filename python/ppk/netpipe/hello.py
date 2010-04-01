#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE for details
# Part of the PPK project

import ppk

import struct

CODE_READ = 1
CODE_WRITE = 2
CODE_LIST = 4

HELLO_LIST = struct.pack("!BI", CODE_LIST, 0)

def flag(truth, value):
    if truth:
        return value
    return 0

def hasFlag(flags, flag):
    return (flags & flag) == flag

def encodeIOHello(channel, read, write):
    out = ppk.Writer()

    code = flag(read, CODE_READ) | flag(write, CODE_WRITE)
    out.writeStruct("!B", code)
    out.writeString(channel)

    return out.finish()

def encodeListHello():
    return HELLO_LIST

def decodeHello(packet):
    pi = ppk.Reader(packet)

    code = pi.readStruct("!B")[0]
    channel = pi.readString()

    read = hasFlag(code, CODE_READ)
    write = hasFlag(code, CODE_WRITE)
    list = hasFlag(code, CODE_LIST)

    return (channel, read, write, list)
