#!/usr/bin/env python

# Copyright (c) 2009 Dmitri Nikulin
# See LICENSE for details
# Part of the PPK project

def tryAdd(items, item):
    if not items.count(item):
        items.append(item)
        return True
    return False

def tryDel(items, item):
    if items.count(item):
        items.remove(item)
        return True
    return False

class Channel(object):
    def __init__(self, name):
        self.name = name
        self.clients = []
        self.readers = []
        self.writers = []

        self.totalObjects = 0
        self.totalBytes = 0

    def addClient(self, client):
        if tryAdd(self.clients, client):
            if client.enableRead:
                tryAdd(self.readers, client)

            if client.enableWrite:
                tryAdd(self.writers, client)

    def removeClient(self, client):
        tryDel(self.clients, client)
        tryDel(self.readers, client)
        tryDel(self.writers, client)

    def sendPacket(self, packet, fromClient=None):
        self.totalObjects += 1
        self.totalBytes += len(packet)

        for writer in self.writers:
            if writer is not fromClient:
                writer.sendPacket(packet)
