// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_NET_PACKET_HH__
#define __PPK_NET_PACKET_HH__

#include <sstream>

#include <ppk/writer.hh>

namespace ppk {

class Packet {
public:

    Packet();
    Packet(uint8_t code);
    ~Packet();

    ppk::Writer &writer() {
        return m_writer;
    }

    void finish(std::string &out) const;

private:

    std::ostringstream m_stream;
    ppk::Writer m_writer;
};

}

#endif /* __PPK_NET_PACKET_HH__ */
