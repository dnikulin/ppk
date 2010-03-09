// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_INOUT_HH__
#define __PPK_INOUT_HH__

#include "ppk/object.hh"

#include <sstream>

#include <boost/iostreams/device/array.hpp>
#include <boost/iostreams/stream.hpp>

#define PPK_BIND_INOUT(T) \
namespace ppk { \
template<> void encode(ppk::Packet &out, const T &obj) { \
    out.clear(); \
    std::ostringstream sout; \
    obj.writeOut(sout); \
    out = Packet(sout.str()); \
} \
template<> void decode(const ppk::Packet &in, T &obj) { \
    namespace io = boost::iostreams; \
    io::stream<io::array_source> buf(in.chars(), in.size()); \
    buf.exceptions(~std::ios::goodbit); \
    try {obj.readIn(buf);} \
    catch (std::ios_base::failure &ex) { \
        std::string er(ex.what()); \
        throw FormatError(er);} \
} \
}

#endif /* __PPK_INOUT_HH__ */
