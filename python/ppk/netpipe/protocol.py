# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE for details
# Part of the PPK project

import ppk
from hello import encodeIOHello, encodeListHello, decodeHello
from listpacket import readListPacket

from twisted.internet.protocol import Protocol
from twisted.protocols.basic import _PauseableMixin

import struct

HEAD_FORMAT = "!I"
HEAD_STRUCT = struct.Struct(HEAD_FORMAT)
HEAD_SIZE = struct.calcsize(HEAD_FORMAT)

DEFAULT_PORT = 32700

class NetPipeProtocol(Protocol, _PauseableMixin):
    def __init__(self):
        self.ibuffer = ''
        self.enableWrite = True
        self.enableRead = True

    def packetReceived(self, packet):
        raise NotImplementedError()

    def dataReceived(self, data):
        if not self.enableRead:
            return

        self.ibuffer += data

        while len(self.ibuffer) >= HEAD_SIZE and not self.paused:
            head = self.ibuffer[:HEAD_SIZE]
            size = HEAD_STRUCT.unpack(head)[0]

            totalSize = HEAD_SIZE + size

            if len(self.ibuffer) < totalSize:
                break

            # NB: 'body' includes 'head'
            body = self.ibuffer[:totalSize]
            self.ibuffer = self.ibuffer[totalSize:]

            self.packetReceived(body)

    def sendPacket(self, headbody):
        try:
            if self.enableWrite:
                self.transport.write(headbody)
        except Exception, er:
            ppk.report("sendPacket: %s" % str(er))

    def sendPacketBody(self, body):
        try:
            if self.enableWrite:
                head = HEAD_STRUCT.pack(len(body))
                self.transport.write(head)
                self.transport.write(body)
        except Exception, er:
            ppk.report("sendPacketBody: %s" % str(er))


class ServerToClientProtocol(NetPipeProtocol):
    def __init__(self, server):
        NetPipeProtocol.__init__(self)
        self.server = server
        self.channel = None
        self.haveHello = False

    def packetReceived(self, packet):
        assert len(packet) >= HEAD_SIZE

        if self.haveHello:
            self.objectReceived(packet)
        else:
            self.helloReceived(packet[HEAD_SIZE:])

    def helloReceived(self, packet):
        assert self.channel is None
        assert not self.haveHello
        self.haveHello = True

        channel, read, write, list = decodeHello(packet)

        if list:
            self.writeList()
            return

        self.channel = self.server.getChannel(channel)
        self.enableRead = read
        self.enableWrite = write

        self.channel.addClient(self)

    def objectReceived(self, packet):
        assert self.channel is not None
        assert self.haveHello

        self.channel.sendPacket(packet, self)

    def writeList(self):
        self.sendPacketBody(self.server.makeListPacket())

    def connectionLost(self, reason):
        if self.channel is not None:
            self.channel.removeClient(self)
            self.enableRead = False
            self.enableWrite = False
            self.ibuffer = None


class ClientToServerProtocol(NetPipeProtocol):
    def __init__(self, channel, read, write, callback):
        NetPipeProtocol.__init__(self)
        # Note: swapped read and write!
        self.hello = encodeIOHello(channel, write, read)
        self.callback = callback

        self.enableRead = read
        self.enableWrite = write

        self.helloSent = False

    def connectionMade(self):
        assert not self.helloSent
        enableWrite = self.enableWrite
        self.enableWrite = True
        self.sendPacketBody(self.hello)
        self.helloSent = True
        self.enableWrite = enableWrite

    def packetReceived(self, packet):
        assert self.enableRead
        assert len(packet) >= HEAD_SIZE

        if self.callback is not None:
            self.callback(packet)


class ListToServerProtocol(NetPipeProtocol):
    def __init__(self, callback):
        NetPipeProtocol.__init__(self)
        self.callback = callback
        self.helloSent = False

    def connectionMade(self):
        assert not self.helloSent
        self.sendPacketBody(encodeListHello())
        self.helloSent = True
        self.enableWrite = False
        self.enableRead = True

    def packetReceived(self, packet):
        assert self.enableRead
        assert len(packet) >= HEAD_SIZE

        if self.callback is not None:
            stats = readListPacket(packet[HEAD_SIZE:])
            self.callback(stats)


class StdioProtocol(NetPipeProtocol):
    def __init__(self, read, write, callback):
        NetPipeProtocol.__init__(self)
        self.callback = callback

        self.enableRead = read
        self.enableWrite = write

    def packetReceived(self, packet):
        assert self.enableRead
        assert len(packet) >= HEAD_SIZE

        if self.callback is not None:
            self.callback(packet)

        self.sendPacket(packet)
