// Copyright (c) 2009 Dmitri Nikulin
// See LICENSE-MIT.txt for details
// Part of the PPK project

#ifndef __PPK_TOOLS_HH__
#define __PPK_TOOLS_HH__

#define PPK_UNUSED(x) ((void)(x))

// A macro to disallow the copy constructor and operator= functions
// This should be used in the private: declarations for a class
#define PPK_NO_COPY(TypeName) \
    TypeName(const TypeName &);       \
    void operator =(const TypeName &)

#endif /* __PPK_TOOLS_HH__ */
