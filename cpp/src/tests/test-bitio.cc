// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#include <ppk/reader.hh>
#include <ppk/writer.hh>

#include <sstream>

#include <boost/test/unit_test.hpp>

static uint64_t kZero64 = (uint64_t)0;
static uint64_t kOne64 = (uint64_t)1;
static uint64_t kFull64 = ~kZero64;

BOOST_AUTO_TEST_SUITE(ppk_bitio)

BOOST_AUTO_TEST_CASE(bitio_test) {
    std::ostringstream os;
    ppk::Writer out(os);

    out.putBits(7, 73);
    out.putBits(2, 1);
    out.putBits(52, 916235);
    out.putBits(64, 1237512);
    out.putBits(64, kFull64);
    out.flushBits();

    std::istringstream is(os.str());
    ppk::Reader in(is);

    BOOST_CHECK_EQUAL(in.getBits(7), 73);
    BOOST_CHECK_EQUAL(in.getBits(2), 1);
    BOOST_CHECK_EQUAL(in.getBits(52), 916235);
    BOOST_CHECK_EQUAL(in.getBits(64), 1237512);
    BOOST_CHECK_EQUAL(in.getBits(64), kFull64);
}

BOOST_AUTO_TEST_SUITE_END()
