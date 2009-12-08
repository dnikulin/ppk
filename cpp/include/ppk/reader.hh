// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_READER_HH__
#define __PPK_READER_HH__

#include "ppk/packet.hh"
#include "ppk/swap.hh"

#include <istream>

#include <stdint.h>

namespace ppk {

class Reader {
public:

    Reader(std::istream &in)
    : m_in(in), m_byte(0), m_bit(8) {
        m_in.exceptions(kStreamFlags);
    }

    uint64_t getBits(uint8_t bits);
    void skipBits();

    uint8_t get() {
        skipBits();
        return m_in.get();
    }

    void get(void *bytes, size_t count) {
        skipBits();

        char *str = reinterpret_cast<char *>(bytes);
        m_in.read(str, count);
    }

    template<class T>
    T getItem() {
        T out;
        uint8_t bytes[sizeof(T)];
        get(bytes, sizeof(T));
        swap<T>(&out, bytes);
        return out;
    }

    template<class T>
    void getItems(T *values, size_t count) {
        uint8_t bytes[sizeof(T)];

        for (size_t i = 0; i < count; i++) {
            get(bytes, sizeof(T));
            swap<T>(values + i, bytes);
        }
    }

    template<class T, class CT>
    void getString(std::basic_string<T> &str) {
        size_t len = getItem<CT>();
        str.resize(len);
        getItems<T>(&str[0], len);
    }

    template<class T>
    void getString(std::basic_string<T> &str) {
        getString<T, uint32_t>(str);
    }

private:

    std::istream &m_in;

    uint8_t m_byte;
    uint8_t m_bit;
};

}

#endif /* __PPK_READER_HH__ */
