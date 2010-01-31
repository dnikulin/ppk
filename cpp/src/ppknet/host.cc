// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/net/host.hh"

#include <boost/bind.hpp>

namespace ppk {

Host::Host(boost::asio::io_service &ios, int port)
    : m_endpoint(boost::asio::ip::tcp::v4(), port),
      m_acceptor(ios, m_endpoint) {
}

Host::~Host() {
}

void Host::startAccepting() {
    SharedLink link = createLink();

    m_acceptor.async_accept(link->socket(),
            boost::bind(&Host::accepted, this,
                link, boost::asio::placeholders::error));
}

void Host::accepted(SharedLink link, const boost::system::error_code &error) {
    startAccepting();

    if (error) {
        link->errored(error);
        return;
    }

    link->connected();
}

}
