// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_WRITER_HH__
#define __PPK_WRITER_HH__

#include "ppk/swap.hh"

#include <ostream>

#include <stdint.h>

namespace ppk {

class Writer {
public:

    Writer(std::ostream &out)
    : m_out(out), m_byte(0), m_bit(0) {}

    void putBits(uint8_t bits, uint64_t value);
    void flushBits();

    void put(uint8_t byte) {
        flushBits();
        m_out.put(byte);
    }

    void put(const void *bytes, size_t count) {
        flushBits();

        const char *str = reinterpret_cast<const char *>(bytes);
        m_out.write(str, count);
    }

    template<class T>
    void putItem(T value) {
        uint8_t bytes[sizeof(T)];
        swap<T>(bytes, &value);
        put(bytes, sizeof(T));
    }

    template<class T>
    void putItems(const T *values, size_t count) {
        for (size_t i = 0; i < count; i++)
            putItem(values[i]);
    }

    template<class T, class CT>
    void putString(const std::basic_string<T> &str) {
        putItem<CT>(static_cast<CT>(str.length()));
        putItems<T>(&str[0], str.length());
    }

    template<class T>
    void putString(const std::basic_string<T> &str) {
        putString<T, uint32_t>(str);
    }

private:

    std::ostream &m_out;

    uint8_t m_byte;
    uint8_t m_bit;
};

}

#endif /* __PPK_WRITER_HH__ */
