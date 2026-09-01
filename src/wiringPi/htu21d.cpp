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
#include "wiringPi/htu21d.h"
}

namespace nb = nanobind;

NB_MODULE(htu21d, m) {
  m.doc() = "nanobind bindings for wiringPi/htu21d.h";
  m.def("htu21d_setup", &htu21dSetup, nb::arg("pin_base"));


}
