// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_OBJECT_HH__
#define __PPK_OBJECT_HH__

#include "ppk/packet.hh"

namespace ppk {

// Encoding template functions
template<class T> void encode(Packet &out, const T &obj);
template<class T> void decode(const Packet &in, T &obj);

// High-level encoded routines
template<class T>
bool pull(T &obj) {
    Packet in;
    if (pullPacket(in) == true) {
        decode(in, obj);
        return true;
    }
    return false;
}

template<class T>
void push(T const &obj) {
    Packet out;
    encode(out, obj);
    pushPacket(out);
}

}

#endif /* __PPK_OBJECT_HH__ */
