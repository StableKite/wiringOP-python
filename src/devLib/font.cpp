// Generated from api_manifest.json. Do not edit directly.
#include <nanobind/nanobind.h>
#include <nanobind/ndarray.h>
#include <Python.h>
#include <algorithm>
#include <array>
#include <cerrno>
#include <condition_variable>
#include <cstdint>
#include <cstring>
#include <dlfcn.h>
#include <mutex>
#include <stdexcept>
#include <string>
#include <vector>
#include <unistd.h>
extern "C" {
#include "devLib/font.h"
}

namespace nb = nanobind;

NB_MODULE(font, m) {
  m.doc() = "nanobind bindings for devLib/font.h";
  m.attr("font_height")=nb::cast(fontHeight);
  m.attr("font_width")=nb::cast(fontWidth);
  m.attr("font")=nb::bytes(reinterpret_cast<const char *>(&font[0]),2048);

}
