// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_INOUT_HH__
#define __PPK_INOUT_HH__

#include "ppk/object.hh"

#include <sstream>

#define PPK_BIND_INOUT(T) \
namespace ppk { \
template<> void encode(std::string &out, const T &obj) { \
    std::ostringstream sout; \
    obj.writeOut(sout); \
    sout.str().swap(out); \
} \
template<> void decode(const std::string &in, T &obj) { \
    std::istringstream sin(in); \
    sin.exceptions(~std::ios::goodbit); \
    try {obj.readIn(sin);} \
    catch (std::ios_base::failure &ex) { \
        std::string er(ex.what()); \
        throw FormatError(er);} \
} \
}

#endif /* __PPK_INOUT_HH__ */
