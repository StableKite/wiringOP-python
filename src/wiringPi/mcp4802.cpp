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
#include "wiringPi/mcp4802.h"
}

namespace nb = nanobind;

NB_MODULE(mcp4802, m) {
  m.doc() = "nanobind bindings for wiringPi/mcp4802.h";
  m.def("mcp4802_setup", &mcp4802Setup, nb::arg("pin_base"), nb::arg("spi_channel"));


}
