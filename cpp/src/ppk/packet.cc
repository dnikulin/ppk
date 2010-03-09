// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/packet.hh"

#include <cassert>
#include <cstring>
#include <stdexcept>

namespace ppk {

struct PacketData {
    volatile int32_t refs;
    uint32_t size;
    uint8_t bytes[];
};

static PacketData kBlankPacket = {1, 0, {}};

Packet::Packet() {
    reset();
}

Packet::Packet(uint32_t size) {
    resize(size);
}

Packet::Packet(uint32_t size, const void *data) {
    resize(size);
    memcpy(m_data->bytes, data, size);
}

Packet::Packet(const std::string &str) {
    resize(str.size());
    memcpy(m_data->bytes, str.data(), str.size());
}

Packet::~Packet() {
}

void Packet::resize(uint32_t size) {
    reset();

    size_t totalSize = sizeof(PacketData) + size;

    void *ptr = malloc(totalSize);
    if (ptr == NULL)
        throw std::bad_alloc();

    PacketData *pack = reinterpret_cast<PacketData *>(ptr);
    assert (pack != NULL);

    pack->refs = 1;
    pack->size = size;

    m_data.reset(pack);
    assert (m_data.get() == pack);
    assert (m_data->refs == 2);
    pack->refs -= 1;
    assert (m_data->refs == 1);
}

void Packet::clear() {
    m_data.reset(&kBlankPacket);
}

void Packet::reset() {
    clear();
}

size_t Packet::size() const {
    return m_data->size;
}

uint8_t *Packet::bytes() {
    return m_data->bytes;
}

const uint8_t *Packet::bytes() const {
    return m_data->bytes;
}

char *Packet::chars() {
    return reinterpret_cast<char *>(bytes());
}

const char *Packet::chars() const {
    return reinterpret_cast<const char *>(bytes());
}

}

namespace boost {

void intrusive_ptr_add_ref(ppk::PacketData *pack) {
    int32_t now = __sync_add_and_fetch(&pack->refs, 1);
    assert (now > 1);
}

void intrusive_ptr_release(ppk::PacketData *pack) {
    int32_t now = __sync_sub_and_fetch(&pack->refs, 1);
    assert (now >= 0);

    if (now < 1)
        free(pack);
}

}
