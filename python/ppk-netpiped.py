#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE for details
# Part of the PPK project

import ppk
from ppk.netpipe.server import NetPipeServer
from ppk.netpipe.protocol import DEFAULT_PORT

from twisted.internet import reactor

from optparse import OptionParser

import os
import sys

def parseOptions():
    parser = OptionParser()
    add = parser.add_option

    add("-p", "--port", dest="port", type="int",
        help="Listen on this TCP port", default=DEFAULT_PORT)

    (options, args) = parser.parse_args()
    return options.port

if __name__ == '__main__':
    port = parseOptions()

    server = NetPipeServer()

    reactor.listenTCP(port, server)
    reactor.run()
