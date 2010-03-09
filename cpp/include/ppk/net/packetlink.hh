// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_NET_PACKETLINK_HH__
#define __PPK_NET_PACKETLINK_HH__

#include "ppk/net/link.hh"
#include "ppk/packet.hh"

#include <deque>
#include <sstream>

#include <boost/enable_shared_from_this.hpp>

namespace ppk {

class PacketLink :
    public Link,
    public boost::enable_shared_from_this<PacketLink> {

public:

    PacketLink(boost::asio::io_service &ios);
    virtual ~PacketLink();

    void writePacket(const Packet &packet);
    void writePacket(const std::ostringstream &stream);

    void startReading();

protected:

    static const uint32_t kBadPacketSize = ~(uint32_t)0;

    void havePacketSize(const boost::system::error_code &error, size_t size);
    void havePacket(const boost::system::error_code &error, size_t size);

    void wrotePacketSize(const boost::system::error_code &error, size_t size);
    void wrotePacket(const boost::system::error_code &error, size_t size);
    void startWriting();

    virtual void readPacket(const Packet &packet) = 0;

    bool m_reading;
    bool m_writing;

    uint32_t m_insize;
    uint32_t m_outsize;

    Packet m_inbound;
    std::deque<Packet> m_outbound;
};

}

#endif /* __PPK_NET_PACKETLINK_HH__ */
