# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

'''
Low-level packet IO.
Abstracts packet header format.
'''

import struct
import sys

__all__ = ["packHead", "unpackHead",
           "fixInputMode", "fixOutputMode",
           "readOneRaw", "readRaw",
           "writeRaw", "writeSizedRaw",
           "wrapBody", "getBody"]

__FixedIn = False
__FixedOut = False

HeadFormat = "!I"
HeadStruct = struct.Struct(HeadFormat)
HeadSize = struct.calcsize(HeadFormat)

def packHead(size):
    '''
    packHead(size) -> head
    Generate packet header from packet body size.
    '''
    return HeadStruct.pack(size)

def unpackHead(head):
    '''
    unpackHead(head) -> size
    Interpret packet header to packet body size.
    '''
    return HeadStruct.unpack(head)[0]

def fixInputMode():
    '''
    Set stdin mode to binary (Windows only)
    '''
    global __FixedIn
    if (not __FixedIn) and (sys.platform == "win32"):
        os = __import__("os")
        msvcrt = __import__("msvcrt")
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        __FixedIn = True

def fixOutputMode():
    '''
    Set stdout mode to binary (Windows only)
    '''
    global __FixedOut
    if (not __FixedOut) and (sys.platform == "win32"):
        os = __import__("os")
        msvcrt = __import__("msvcrt")
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
        __FixedOut = True

def readOneRaw(fd = sys.stdin):
    '''
    readOneRaw(fd = sys.stdin) -> (head, body)
    Read one packet, returning its head and body bytes.
    Raises EOFError if bytes are unavailable.
    '''
    fixInputMode()

    head = fd.read(HeadSize)
    if len(head) < HeadSize:
        raise EOFError()

    size = unpackHead(head)

    body = fd.read(size)
    if len(body) != size:
        raise EOFError()

    return (head, body)

def readRaw(fd = sys.stdin):
    '''
    readRaw(fd = sys.stdin) -> generator(head, body)
    Read packets, returning their head and body bytes.
    Returns after the first EOFError.
    '''
    try:
        while True:
            yield readOneRaw(fd)
    except (EOFError, IOError):
        pass

def writeRaw(body, fd = sys.stdout):
    '''
    Write one packet, generating head bytes.
    Calls fd.flush() if available.
    '''
    fixOutputMode()
    head = packHead(len(body))
    fd.write(head)
    fd.write(body)

    try:
        fd.flush()
    except AttributeError:
        pass

def writeSizedRaw(headbody, fd = sys.stdout):
    '''
    Write one packet, using prepended head bytes.
    Calls fd.flush() if available.
    '''
    fixOutputMode()
    fd.write(headbody)

    try:
        fd.flush()
    except AttributeError:
        pass

def wrapBody(body):
    '''
    wrapBody(body) -> headbody
    Prepend head bytes to body bytes.
    '''
    return packHead(len(body)) + body

def getBody(headbody):
    '''
    getBody(headbody) -> body
    Extract body bytes from headered packet.
    '''
    return headbody[HeadSize:]
