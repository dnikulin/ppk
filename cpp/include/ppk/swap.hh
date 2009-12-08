// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_SWAP_HH__
#define __PPK_SWAP_HH__

#include <stdint.h>

#include <cstddef>
#include <cstring>

#include <endian.h>

namespace ppk {

template<int N>
void swapBytes(void *out, const void *in) {
    uint8_t *ob = reinterpret_cast<uint8_t *>(out);
    const uint8_t *ib = reinterpret_cast<const uint8_t *>(in);

#ifdef PPK_LITTLE_ENDIAN
    for (int i = 0; i < N; i++)
        ob[i] = ib[N - i - 1];
#else
    for (int i = 0; i < N; i++)
        ob[i] = ib[i];
#endif
}

template<int N>
void swapBytes(void *out, const void *in, size_t m) {
    uint8_t *ob = reinterpret_cast<uint8_t *>(out);
    const uint8_t *ib = reinterpret_cast<const uint8_t *>(in);

#ifdef PPK_LITTLE_ENDIAN
    for (unsigned j = 0, o = 0; j < m; j++) {
        for (int i = 0; i < N; i++, o += N)
            ob[o + i] = ib[o + N - i - 1];
    }
#else
    for (int i = 0; i < (N * m); i++)
        ob[i] = ib[i];
#endif
}

template<class T>
void swap(void *out, const void *in) {
    swapBytes<sizeof(T)>(out, in);
}

template<class T>
void swap(void *out, const void *in, size_t m) {
    swapBytes<sizeof(T)>(out, in, m);
}

template<class T>
T swap(T in) {
    T out;
    swapBytes<sizeof(T)>(&out, &in);
    return out;
}

}

#endif /* __PPK_SWAP_HH__ */
