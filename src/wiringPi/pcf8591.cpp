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
#include "wiringPi/pcf8591.h"
}

namespace nb = nanobind;

NB_MODULE(pcf8591, m) {
  m.doc() = "nanobind bindings for wiringPi/pcf8591.h";
  m.def("pcf8591_setup", &pcf8591Setup, nb::arg("pin_base"), nb::arg("i2c_address"));


}
