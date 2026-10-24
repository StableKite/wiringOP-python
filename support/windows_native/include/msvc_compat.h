/*
 * Native MSVC C ABI declarations for compiling the hardware-free Windows
 * validation backend against the exact, unchanged Linux wiringOP headers.
 *
 * Only `unused` and `format(printf, ..., ...)` GCC diagnostics appear in the
 * reviewed public headers; the CI guard rejects any new attribute category.
 * These diagnostics have no ABI/storage-layout effects. Never suppress a
 * packed, aligned, calling-convention, or other semantic attribute here.
 */
#ifndef WIRINGOP_MSVC_COMPAT_H
#define WIRINGOP_MSVC_COMPAT_H
#if defined(_MSC_VER) && !defined(__clang__)
#  include <BaseTsd.h>
#  ifndef _SSIZE_T_DEFINED
     typedef SSIZE_T ssize_t;
#    define _SSIZE_T_DEFINED 1
#  endif
#  ifndef __attribute__
#    define __attribute__(annotation)
#  endif
#endif
#endif
