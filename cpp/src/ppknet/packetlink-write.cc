// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/net/packetlink.hh"

#include <cassert>

#include <boost/bind.hpp>

#include <ppk/swap.hh>

namespace ppk {

void PacketLink::writePacket(const std::string &body) {
    m_outbound.push_back(body);
    startWriting();
}

void PacketLink::writePacket(const Packet &packet) {
    static const std::string blank;
    m_outbound.push_back(blank);
    packet.finish(m_outbound.back());
    startWriting();
}

void PacketLink::startWriting() {
    if (m_writing == true)
        return;

    if (m_socket.is_open() == false)
        return;

    assert (m_outsize == kBadPacketSize);

    if (m_outbound.empty() == true)
        return;

    const std::string &packet(m_outbound.front());
    m_outsize = ppk::swap<uint32_t>(packet.size());

    m_writing = true;

    boost::asio::async_write(m_socket,
            boost::asio::buffer(&m_outsize, sizeof(m_outsize)),
            boost::bind(&PacketLink::wrotePacketSize, shared_from_this(),
                    boost::asio::placeholders::error,
                    boost::asio::placeholders::bytes_transferred));
}

void PacketLink::wrotePacketSize(const boost::system::error_code &error, size_t size) {
    if (error) {
        errored(error);
        return;
    }

    assert (m_writing == true);
    assert (m_outsize != kBadPacketSize);
    assert (m_outbound.empty() == false);
    assert (size == sizeof(m_outsize));

    const std::string &packet(m_outbound.front());

    // Skip writing empty packet
    if (packet.size() == 0) {
        wrotePacket(error, 0);
        return;
    }

    boost::asio::async_write(m_socket,
            boost::asio::buffer(packet),
            boost::bind(&PacketLink::wrotePacket, shared_from_this(),
                    boost::asio::placeholders::error,
                    boost::asio::placeholders::bytes_transferred));
}

void PacketLink::wrotePacket(const boost::system::error_code &error, size_t size) {
    if (error) {
        errored(error);
        return;
    }

    assert (m_writing == true);
    assert (m_outsize != kBadPacketSize);
    assert (m_outbound.empty() == false);

    assert (size == m_outbound.front().size());
    assert (size == ppk::swap<uint32_t>(m_outsize));

    m_writing = false;
    m_outsize = kBadPacketSize;
    m_outbound.pop_front();

    startWriting();
}

}
