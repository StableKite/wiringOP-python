/*
 * Native Win32 symbol lookup for the optional RTLD_DEFAULT declarations
 * exposed by the wiringPi bindings. No fabricated symbols or return values.
 * The actual exported symbols are searched in every loaded process module.
 */
#ifndef WIRINGOP_NATIVE_DLFCN_H
#define WIRINGOP_NATIVE_DLFCN_H
#if !defined(_WIN32)
#  error "This header must never replace POSIX dlfcn.h"
#endif
#include <windows.h>
#include <psapi.h>

#ifndef RTLD_DEFAULT
#  define RTLD_DEFAULT ((void *) 0)
#endif

#ifdef __cplusplus
static inline void *dlsym(void *handle, const char *symbol) noexcept {
    if (handle != RTLD_DEFAULT || symbol == nullptr) {
        return nullptr;
    }
    HMODULE modules[1024] = {};
    DWORD needed = 0;
    if (!K32EnumProcessModules(GetCurrentProcess(), modules, sizeof(modules), &needed)) {
        return nullptr;
    }
    if (needed > sizeof(modules)) {
        return nullptr;  /* Incomplete inventory: fail closed. */
    }
    for (size_t i = 0; i < needed / sizeof(HMODULE); ++i) {
        FARPROC address = GetProcAddress(modules[i], symbol);
        if (address != nullptr) {
            return reinterpret_cast<void *>(address);
        }
    }
    return nullptr;
}
#endif
#endif
