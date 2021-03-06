// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/net/link.hh"

#include <cassert>
#include <iostream>

namespace ppk {

Link::Link(boost::asio::io_service &ios) : m_socket(ios) {
}

Link::~Link() {
}

void Link::connect(const std::string &host, const std::string &port) {
    findHost(m_socket, host, port);
    connected();
}

void Link::disconnect() {
    if (m_socket.is_open() == true) {
        m_socket.close();
        disconnected();
    }
}

void Link::connected() {
}

void Link::disconnected() {
}

void Link::errored(const boost::system::error_code &error) {
    disconnect();
}

}
