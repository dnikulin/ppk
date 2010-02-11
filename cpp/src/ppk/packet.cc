// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/packet.hh"
#include "ppk/swap.hh"

#include <cstring>
#include <iostream>

#include <stdint.h>

namespace ppk {

static bool works(const std::istream &in) {
    return (in.bad() || in.eof() || in.fail()) == false;
}

bool pullPacket(std::string &out, std::istream &in) {
    if (works(in)) {
        out.clear();

        char head[sizeof(uint32_t)] = {0,};
        in.read(head, sizeof(head));

        if (works(in)) {
            uint32_t size = 0;
            swapBytes<sizeof(head)>(&size, head);

            out.resize(size);
            in.read(&out[0], size);

            return works(in);
        }
    }

    return false;
}

void pushPacket(const std::string &in, std::ostream &out) {
    const uint32_t size = in.size();

    char head[sizeof(size)] = {0,};
    swapBytes<sizeof(head)>(head, &size);

    out.write(head, sizeof(head));
    out.write(&in[0], size);
}

bool pullPacket(std::string &out) {
    return pullPacket(out, std::cin);
}

void pushPacket(const std::string &in) {
    pushPacket(in, std::cout);
    std::cout.flush();
}

void wrapPacket(std::string &out, const std::string &in) {
    const uint32_t size = in.size();

    out.resize(size + sizeof(uint32_t));

    swap<uint32_t>(&out[0], &size);
    memcpy(&out[sizeof(uint32_t)], &in[0], size);
}

}
