// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_BOOSTED_HH__
#define __PPK_BOOSTED_HH__

#include "ppk/object.hh"

#include <sstream>

#include <boost/serialization/serialization.hpp>
#include <boost/archive/binary_iarchive.hpp>
#include <boost/archive/binary_oarchive.hpp>

namespace ppk {

template<class T>
void encodeBoosted(std::string &out, const T &obj) {
    out.clear();
    std::ostringstream stream(std::ios::binary);
    {
        using namespace boost::archive;
        binary_oarchive arch(stream, no_header);
        arch & obj;
    }
    stream.str().swap(out);
}

template<class T>
void decodeBoosted(const std::string &in, T &obj) {
    using namespace boost::archive;
    std::istringstream stream(in, std::ios::binary);
    binary_iarchive arch(stream, no_header);
    arch & obj;
}

#define PPK_BIND_BOOSTED(T) \
namespace ppk { \
template<> void encode(std::string &out, const T &obj) \
    { encodeBoosted(out, obj); } \
template<> void decode(const std::string &in, T &obj) \
    { decodeBoosted(in, obj); } \
}

}

#endif /* __PPK_BOOSTED_HH__ */
