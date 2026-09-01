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
#include "wiringPi/mcp23017.h"
}

namespace nb = nanobind;

NB_MODULE(mcp23017, m) {
  m.doc() = "nanobind bindings for wiringPi/mcp23017.h";
  m.def("mcp23017_setup", &mcp23017Setup, nb::arg("pin_base"), nb::arg("i2c_address"));


}
