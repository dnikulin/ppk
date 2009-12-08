#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

'''
Utility functions supporting filter modules.
'''

import cPickle
import hashlib
import sys
import zlib

__all__ = ["enpickle", "depickle",
           "enpicklegz", "depicklegz",
           "hashBody", "hashBodyHex",
           "report", "printUsage",
           "percent"]

def enpickle(obj):
    '''
    Encoder using pickle format.
    '''
    return cPickle.dumps(obj)

def depickle(body):
    '''
    Decoder using pickle format.
    '''
    return cPickle.loads(body)

def enpicklegz(obj):
    '''
    Encoder using pickle format with gzip compression.
    '''
    return zlib.compress(enpickle(obj), 9)

def depicklegz(body):
    '''
    Decoder using pickle format with gzip compression.
    '''
    return depickle(zlib.decompress(body))

def hashBody(body):
    '''
    hashBody(body) -> binary hash string
    Hash packet body (SHA256).
    '''
    return hashlib.sha256(body).digest()

def hashBodyHex(body):
    '''
    hashBodyHex(body) -> hex hash string
    Hash packet body (SHA256), returning hex string.
    '''
    return hashlib.sha256(body).hexdigest()

def report(line):
    '''
    Print line to stderr, including program name.
    '''
    print >> sys.stderr, "%s: %s" % (sys.argv[0], line)

def printUsage(line = ""):
    '''
    Print usage line to stderr, exit with code 1.
    '''
    print >> sys.stderr, "usage: %s %s" % (sys.argv[0], line)
    sys.exit(1)

def percent(some, of):
    '''
    Calculcate percentage of numeric types.
    Returns 0 if of is 0.
    '''
    if of != 0:
        return int((some * 100) // of)
    return 0
