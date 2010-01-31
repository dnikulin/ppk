// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/net/packet.hh"

namespace ppk {

Packet::Packet() : m_writer(m_stream) {
}

Packet::Packet(uint8_t code) : m_writer(m_stream) {
    m_writer.put(code);
}

Packet::~Packet() {
}

void Packet::finish(std::string &out) const {
    m_stream.str().swap(out);
}

}
