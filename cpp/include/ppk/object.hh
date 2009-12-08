// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_OBJECT_HH__
#define __PPK_OBJECT_HH__

#include "ppk/packet.hh"

namespace ppk {

// Encoding template functions
template<class T> void encode(std::string &out, const T &obj);
template<class T> void decode(const std::string &in, T &obj);

// High-level encoded routines
template<class T>
bool pull(T &obj) {
    std::string in;
    if (pullPacket(in) == true) {
        decode(in, obj);
        return true;
    }
    return false;
}

template<class T>
void push(T const &obj) {
    std::string out;
    encode(out, obj);
    pushPacket(out);
}

}

#endif /* __PPK_OBJECT_HH__ */
