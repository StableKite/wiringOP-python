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
#include "wiringPi/sr595.h"
}

namespace nb = nanobind;

NB_MODULE(sr595, m) {
  m.doc() = "nanobind bindings for wiringPi/sr595.h";
  m.def("sr595_setup", &sr595Setup, nb::arg("pin_base"), nb::arg("num_pins"), nb::arg("data_pin"), nb::arg("clock_pin"), nb::arg("latch_pin"));


}
