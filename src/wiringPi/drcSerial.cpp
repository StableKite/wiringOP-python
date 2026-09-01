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
#include "wiringPi/drcSerial.h"
}

namespace nb = nanobind;

NB_MODULE(drc_serial, m) {
  m.doc() = "nanobind bindings for wiringPi/drcSerial.h";
  m.def("drc_setup_serial", &drcSetupSerial, nb::arg("pin_base"), nb::arg("num_pins"), nb::arg("device"), nb::arg("baud"));


}
