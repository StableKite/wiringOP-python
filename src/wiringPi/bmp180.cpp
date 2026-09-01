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
#include "wiringPi/bmp180.h"
}

namespace nb = nanobind;

NB_MODULE(bmp180, m) {
  m.doc() = "nanobind bindings for wiringPi/bmp180.h";
  m.def("bmp180_setup", &bmp180Setup, nb::arg("pin_base"));


}
