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
#include "wiringPi/max5322.h"
}

namespace nb = nanobind;

NB_MODULE(max5322, m) {
  m.doc() = "nanobind bindings for wiringPi/max5322.h";
  m.def("max5322_setup", &max5322Setup, nb::arg("pin_base"), nb::arg("spi_channel"));


}
