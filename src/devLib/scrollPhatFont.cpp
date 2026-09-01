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
#include "devLib/scrollPhatFont.h"
}

namespace nb = nanobind;

NB_MODULE(scroll_phat_font, m) {
  m.doc() = "nanobind bindings for devLib/scrollPhatFont.h";
  m.attr("font_height")=nb::cast(fontHeight);
  m.attr("scroll_phat_font")=nb::bytes(reinterpret_cast<const char *>(&scrollPhatFont[0]),320);

}
