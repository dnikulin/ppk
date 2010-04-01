#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE for details
# Part of the PPK project

import ppk

from ppk.netpipe.protocol import ClientToServerProtocol, ListToServerProtocol, StdioProtocol
from ppk.netpipe.protocol import DEFAULT_PORT

from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.internet.stdio import StandardIO

from optparse import OptionParser

import os
import sys

class ClientFactory(ClientFactory):
    def __init__(self, link, stdio):
        self.link = link
        self.stdio = stdio
        link.factory = self

    def buildProtocol(self, addr):
        StandardIO(self.stdio)
        return self.link

class ListFactory(ClientFactory):
    def __init__(self, link):
        self.link = link

    def buildProtocol(self, addr):
        return self.link

def parseOptions():
    parser = OptionParser("usage: %prog [options] [channel]")
    add = parser.add_option

    add("-c", "--host", dest="host",
        help="Connect to this pipe host", default="localhost")
    add("-p", "--port", dest="port", type="int",
        help="Connect on this TCP port", default=DEFAULT_PORT)
    add("-s", "--send", dest="send", action="store_true",
        help="Send objects to the server")
    add("-r", "--recv", dest="recv", action="store_true",
        help="Receive objects from the server")
    add("-l", "--list", dest="list", action="store_true",
        help="List existing channels on the server and exit")

    (options, args) = parser.parse_args()

    channel = ''

    if not options.list:
        if len(args) == 1:
            channel = args[0]
        else:
            parser.error("If not listing, channel name is required")

    return (options.host, options.port,
            options.send, options.recv, options.list,
            channel)

def printList(stats):
    BREAK = "------------------------------------------------------------------"

    print BREAK
    print "Channel                 Inputs   Outputs     Objects           MiB"
    print BREAK

    for parts in stats:
        print ("%-20s  %8d  %8d  %10d  %12d" % parts)

    print BREAK

if __name__ == '__main__':
    host, port, send, recv, list, channel = parseOptions()

    server = None
    factory = None

    if list:
        def readList(stats):
            printList(stats)
            server.transport.loseConnection()
            reactor.stop()

        server = ListToServerProtocol(readList)
        factory = ListFactory(server)
    else:
        stdio = None

        def writeStdout(packet):
            stdio.sendPacket(packet)

        def writeServer(packet):
            server.sendPacket(packet)

        # True, True for stdio so objects pass through
        stdio = StdioProtocol(True, True, writeServer)
        server = ClientToServerProtocol(channel, recv, send, writeStdout)
        factory = ClientFactory(server, stdio)

    reactor.connectTCP(host, port, factory)
    reactor.run()
