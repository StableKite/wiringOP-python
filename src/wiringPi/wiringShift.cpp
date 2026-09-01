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
#include "wiringPi/wiringShift.h"
}

namespace nb = nanobind;

NB_MODULE(wiring_shift, m) {
  m.doc() = "nanobind bindings for wiringPi/wiringShift.h";
  m.def("shift_in", &shiftIn, nb::arg("d_pin"), nb::arg("c_pin"), nb::arg("order"));
  m.def("shift_out", &shiftOut, nb::arg("d_pin"), nb::arg("c_pin"), nb::arg("order"), nb::arg("val"));

  m.attr("LSBFIRST")=nb::cast((LSBFIRST));
  m.attr("MSBFIRST")=nb::cast((MSBFIRST));
}
