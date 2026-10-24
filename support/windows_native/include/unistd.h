/* MSVC's native IO declarations, not a POSIX emulation layer. */
#ifndef WIRINGOP_NATIVE_UNISTD_H
#define WIRINGOP_NATIVE_UNISTD_H
#if !defined(_WIN32)
#  error "This minimal Windows-only include must never shadow POSIX unistd.h"
#endif
#include <io.h>
#include <process.h>
#endif
