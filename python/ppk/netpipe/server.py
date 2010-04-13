# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE for details
# Part of the PPK project

from channel import Channel
from listpacket import makeListPacket
from protocol import ServerToClientProtocol

from twisted.internet.protocol import ServerFactory

class NetPipeServer(ServerFactory):
    def __init__(self):
        self.channels = {}

    def getChannel(self, name):
        if name not in self.channels:
            channel = Channel(name)
            self.channels[name] = channel
            return channel
        return self.channels[name]

    def buildProtocol(self, addr):
        link = ServerToClientProtocol(self)
        link.factory = self
        return link

    def makeListPacket(self):
        return makeListPacket(self.channels.values())
