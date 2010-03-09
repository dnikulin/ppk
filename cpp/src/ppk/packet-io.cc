// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/packet.hh"
#include "ppk/swap.hh"

#include <iostream>

namespace ppk {

bool pullPacket(Packet &out, std::istream &in) {
    out.reset();

    if (in.good() == true) {
        char head[sizeof(uint32_t)] = {0,};
        in.read(head, sizeof(head));

        if (in.good() == true) {
            uint32_t size = 0;
            swapBytes<sizeof(head)>(&size, head);

            out = Packet(size);
            in.read(out.chars(), size);

            return in.good() == true;
        }
    }

    return false;
}

void pushPacket(const Packet &in, std::ostream &out) {
    const uint32_t size = in.size();

    char head[sizeof(size)] = {0,};
    swapBytes<sizeof(head)>(head, &size);

    out.write(head, sizeof(head));
    out.write(in.chars(), size);
}

bool pullPacket(Packet &out) {
    return pullPacket(out, std::cin);
}

void pushPacket(const Packet &in) {
    pushPacket(in, std::cout);
    std::cout.flush();
}

}
