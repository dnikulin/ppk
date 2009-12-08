// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_EXCEPT_HH__
#define __PPK_EXCEPT_HH__

#include <stdexcept>

namespace ppk {

class PosixError : public std::runtime_error {
public:
    explicit PosixError();
    explicit PosixError(int error);
};

class StateError : public std::logic_error {
public:
    explicit StateError(const std::string &arg)
        : std::logic_error(arg) {}
};

class FormatError : public std::range_error {
public:
    explicit FormatError(const std::string &arg)
        : std::range_error(arg) {}
};

void throwFormatError(const char *line);

#define ppk_want(x) \
do { if (!(x)) \
    ppk::throwFormatError("want (" #x ")"); \
} while (0)

}

#endif /* __PPK_EXCEPT_HH__ */
