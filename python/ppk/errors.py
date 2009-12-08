#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE-MIT.txt for details
# Part of the PPK project

'''
Error types.
'''

__all__ = ["FormatError", "expect"]

class FormatError(Exception):
    '''
    Error in packet decoding.
    '''
    pass

def expect(cond):
    '''
    Raise FormatError if cond does not hold.
    '''
    if cond == False:
        raise FormatError()
