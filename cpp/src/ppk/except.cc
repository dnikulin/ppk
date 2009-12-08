// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/except.hh"

#include <cerrno>
#include <cstring>

namespace ppk {

static std::string errstr(int error) {
    return std::string(strerror(error));
}

PosixError::PosixError() : std::runtime_error(errstr(errno)) {}
PosixError::PosixError(int error) : std::runtime_error(errstr(error)) {}

void throwFormatError(const char *line) {
    std::string sline(line);
    throw FormatError(sline);
}

}
