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
#include "wiringPi/sn3218.h"
}

namespace nb = nanobind;

NB_MODULE(sn3218, m) {
  m.doc() = "nanobind bindings for wiringPi/sn3218.h";
  m.def("sn3218_setup", &sn3218Setup, nb::arg("pin_base"));


}
