#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

'''
Convenience functions for encoded packet IO.
'''

from rawio import readOneRaw, readRaw, writeRaw

import sys

__all__ = ["identity",
           "readObject", "writeObject",
           "readObjects", "writeObjects"] 

def identity(body):
    '''
    identity(body) -> body
    Identity encoder/decoder.
    Returns bytes/object as given.
    '''
    return body

def readObject(decoder = identity, fd = sys.stdin):
    '''
    readObject(decoder, fd) -> object
    Read and decode one packet.
    Raises EOFError if bytes are unavailable.
    '''
    return decoder(readOneRaw(fd)[1])

def writeObject(obj, encoder = identity, fd = sys.stdout):
    '''
    Encode and write one packet.
    '''
    writeRaw(encoder(obj), fd)

def readObjects(decoder = identity, fd = sys.stdin):
    '''
    readObjects(decoder, fd) -> generator(object)
    Read and decode packets.
    Returns after the first EOFError.
    '''
    for _, body in readRaw(fd):
        yield decoder(body)

def writeObjects(objs, encoder = identity, fd = sys.stdout):
    '''
    Encode and write packets.
    '''
    for obj in objs:
        writeObject(obj, encoder, fd)
