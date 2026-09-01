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
#include "wiringPi/rht03.h"
}

namespace nb = nanobind;

NB_MODULE(rht03, m) {
  m.doc() = "nanobind bindings for wiringPi/rht03.h";
  m.def("rht03_setup", &rht03Setup, nb::arg("pin_base"), nb::arg("device_pin"));


}
