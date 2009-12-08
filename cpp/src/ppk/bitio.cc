// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include "ppk/reader.hh"
#include "ppk/writer.hh"

#include <cassert>

namespace ppk {

template<class T>
T min(T a, T b) {
    return (a < b) ? a : b;
}

static uint64_t mask64(uint64_t bits) {
    assert (bits <= 64);
    return (((uint64_t) 1) << bits) - 1;
}

uint64_t Reader::getBits(uint8_t bits) {
    assert (m_bit <= 8);
    assert (bits > 0);
    assert (bits <= 64);

    uint64_t out = 0;
    uint8_t done = 0;

    while (done < bits) {
        assert (m_bit <= 8);

        uint8_t more = min(8 - m_bit, bits - done);
        assert (more <= 8);

        if (more == 0) {
            m_byte = m_in.get();
            m_bit = 0;
            continue;
        }

        uint8_t lobits = 8 - (m_bit + more);
        assert (lobits < 8);
        assert ((m_bit + more + lobits) == 8);

        uint8_t value = m_byte >> lobits;

        if (more != 8)
            value &= ((1 << more) - 1);

        uint64_t oldout = out;
        out <<= more;
        assert (out >= oldout);
        assert ((out & value) == 0);

        out |= value;
        m_bit += more;
        done += more;
        assert (done <= bits);
        assert (m_bit <= 8);
    }

    assert ((out & mask64(bits)) == out);
    return out;
}

void Reader::skipBits() {
    m_byte = 0;
    m_bit = 0;
}

void Writer::putBits(uint8_t bits, uint64_t value) {
    assert (m_bit <= 8);
    assert (bits > 0);
    assert (bits <= 64);

    assert ((value & mask64(bits)) == value);

    uint8_t done = 0;

    while (done < bits) {
        assert (m_bit <= 8);

        uint8_t more = min(8 - m_bit, bits - done);
        assert (more <= 8);

        if (more == 0) {
            flushBits();
            continue;
        }

        uint64_t downvalue = value >> (bits - done - more);
        assert (downvalue <= value);
        assert ((downvalue & mask64(bits)) == downvalue);

        uint8_t byte = (uint8_t) (downvalue & mask64(more));
        uint8_t shifted = byte << (8 - m_bit - more);
        assert (shifted >= byte);
        assert ((byte == 0) == (shifted == 0));

        m_byte |= shifted;
        m_bit += more;
        done += more;
        assert (done <= bits);
        assert (m_bit <= 8);

        if (m_bit == 8)
            flushBits();
    }
}

void Writer::flushBits() {
    if (m_bit > 0) {
        m_out.put(m_byte);
        m_byte = 0;
        m_bit = 0;
    }
}

}
