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
#include "wiringPi/ds18b20.h"
}

namespace nb = nanobind;

NB_MODULE(ds18b20, m) {
  m.doc() = "nanobind bindings for wiringPi/ds18b20.h";
  m.def("ds18b20_setup", &ds18b20Setup, nb::arg("pin_base"), nb::arg("serial_num"));


}
