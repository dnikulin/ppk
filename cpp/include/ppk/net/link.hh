// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_NET_LINK_HH__
#define __PPK_NET_LINK_HH__

#include <string>

#include <boost/asio.hpp>

#include <ppk/reader.hh>

namespace ppk {

void findHost(boost::asio::ip::tcp::socket &socket,
        const std::string &host,
        const std::string &port);

class Link {
public:

    Link(boost::asio::io_service &ios);
    virtual ~Link();

    virtual void connected();
    virtual void disconnected();
    virtual void errored(const boost::system::error_code &error);

    void connect(const std::string &host, const std::string &port);
    void disconnect();

    boost::asio::ip::tcp::socket &socket() {
        return m_socket;
    }

    bool isConnected() const {
        return m_socket.is_open();
    }

protected:

    boost::asio::ip::tcp::socket m_socket;
};

}

#endif /* __PPK_NET_LINK_HH__ */
