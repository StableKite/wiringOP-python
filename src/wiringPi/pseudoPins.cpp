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
#include "wiringPi/pseudoPins.h"
}

namespace nb = nanobind;

NB_MODULE(pseudo_pins, m) {
  m.doc() = "nanobind bindings for wiringPi/pseudoPins.h";
  m.def("pseudo_pins_setup", &pseudoPinsSetup, nb::arg("pin_base"));


}
