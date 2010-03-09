// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_PACKET_HH__
#define __PPK_PACKET_HH__

#include <istream>
#include <ostream>
#include <string>

#include <boost/cstdint.hpp>
#include <boost/intrusive_ptr.hpp>

namespace ppk {

struct PacketData;

class Packet {
public:

    Packet();
    Packet(uint32_t size);
    Packet(uint32_t size, const void *data);
    Packet(const std::string &str);
    ~Packet();

    void resize(uint32_t size);
    void clear();
    void reset();

    size_t size() const;

    uint8_t *bytes();
    const uint8_t *bytes() const;

    char *chars();
    const char *chars() const;

private:

    boost::intrusive_ptr<PacketData> m_data;
};

Packet makePacket(uint32_t size);
Packet copyPacket(uint32_t size, const void *data);

// Packet IO routines (any stream)
bool pullPacket(Packet &out, std::istream &in);
void pushPacket(const Packet &in, std::ostream &out);

// Packet IO routines (std::cin, std::cout)
bool pullPacket(Packet &out);
void pushPacket(const Packet &in);

}

namespace boost {
void intrusive_ptr_add_ref(ppk::PacketData *pack);
void intrusive_ptr_release(ppk::PacketData *pack);
}

#endif /* __PPK_PACKET_HH__ */
