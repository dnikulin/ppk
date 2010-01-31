// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/net/link.hh"

namespace ppk {

void findHost(boost::asio::ip::tcp::socket &socket,
        const std::string &host,
        const std::string &port) {

    using namespace boost::asio;
    using namespace boost::asio::ip;

    tcp::resolver resolver(socket.io_service());
    tcp::resolver::query query(host, port);

    tcp::resolver::iterator iter = resolver.resolve(query);
    tcp::resolver::iterator end;

    boost::system::error_code error = error::host_not_found;

    while (error && (iter != end)) {
        socket.close();
        socket.connect(*iter++, error);
    }

    if (error)
        throw boost::system::system_error(error);
}

}
