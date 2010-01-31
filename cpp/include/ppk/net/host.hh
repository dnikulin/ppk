// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_NET_HOST_HH__
#define __PPK_NET_HOST_HH__

#include "ppk/net/packetlink.hh"

#include <boost/asio.hpp>
#include <boost/shared_ptr.hpp>

namespace ppk {

class Host {
public:

    typedef boost::shared_ptr<Link> SharedLink;

    Host(boost::asio::io_service &ios, int port);
    virtual ~Host();

    boost::asio::io_service &ioservice() {
        return m_acceptor.io_service();
    }

    void startAccepting();

protected:

    void accepted(SharedLink link,
            const boost::system::error_code &error);

    virtual SharedLink createLink() = 0;

    boost::asio::ip::tcp::endpoint m_endpoint;
    boost::asio::ip::tcp::acceptor m_acceptor;
};

}

#endif /* __PPK_NET_HOST_HH__ */
