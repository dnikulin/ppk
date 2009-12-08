// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_PACKET_HH__
#define __PPK_PACKET_HH__

#include <istream>
#include <ostream>
#include <string>

namespace ppk {

static const std::ios::iostate kStreamFlags =
        std::ios_base::badbit |
        std::ios_base::eofbit |
        std::ios_base::failbit;

// Packet IO routines (any stream)
bool pullPacket(std::string &out, std::istream &in);
void pushPacket(const std::string &in, std::ostream &out);

// Packet IO routines (std::cin, std::cout)
bool pullPacket(std::string &out);
void pushPacket(const std::string &in);

// Packet wrapper
void wrapPacket(std::string &out, const std::string &in);

}

#endif /* __PPK_PACKET_HH__ */
