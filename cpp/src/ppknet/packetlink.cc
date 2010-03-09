// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/net/packetlink.hh"

namespace ppk {

PacketLink::PacketLink(boost::asio::io_service &ios)
    : Link(ios),
      m_reading(false), m_writing(false),
      m_insize(kBadPacketSize), m_outsize(kBadPacketSize) {
}

PacketLink::~PacketLink() {
}

}
