// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/net/packetlink.hh"

#include <cassert>

#include <boost/bind.hpp>

#include <ppk/swap.hh>

namespace ppk {

static const std::string kBlankString;

void PacketLink::startReading() {
    if (m_reading == true)
        return;

    if (m_socket.is_open() == false)
        return;

    assert (m_insize == kBadPacketSize);
    assert (m_inbound.size() == 0);

    m_reading = true;

    boost::asio::async_read(m_socket,
            boost::asio::buffer(&m_insize, sizeof(m_insize)),
            boost::bind(&PacketLink::havePacketSize, shared_from_this(),
                    boost::asio::placeholders::error,
                    boost::asio::placeholders::bytes_transferred));
}

void PacketLink::havePacketSize(const boost::system::error_code &error, size_t size) {
    if (error) {
        errored(error);
        return;
    }

    assert (m_reading == true);
    assert (m_insize != kBadPacketSize);
    assert (m_inbound.size() == 0);
    assert (size == sizeof(m_insize));

    m_insize = ppk::swap<uint32_t>(m_insize);

    if (m_insize == 0) {
        Packet blank;
        readPacket(blank);
        m_reading = false;
        m_insize = kBadPacketSize;
        startReading();
        return;
    }

    m_inbound.resize(m_insize);

    boost::asio::async_read(m_socket,
            boost::asio::buffer(m_inbound.bytes(), m_insize),
            boost::bind(&PacketLink::havePacket, shared_from_this(),
                    boost::asio::placeholders::error,
                    boost::asio::placeholders::bytes_transferred));
}

void PacketLink::havePacket(const boost::system::error_code &error, size_t size) {
    if (error) {
        errored(error);
        return;
    }

    assert (m_reading == true);
    assert (m_insize != kBadPacketSize);
    assert (m_inbound.size() == m_insize);
    assert (size == m_insize);

    m_reading = false;
    m_insize = kBadPacketSize;

    readPacket(m_inbound);
    m_inbound.clear();

    startReading();
}

}
