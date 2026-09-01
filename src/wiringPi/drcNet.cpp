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
#include "wiringPi/drcNet.h"
}

namespace nb = nanobind;

NB_MODULE(drc_net, m) {
  m.doc() = "nanobind bindings for wiringPi/drcNet.h";
  m.def("drc_setup_net", &drcSetupNet, nb::arg("pin_base"), nb::arg("num_pins"), nb::arg("ip_address"), nb::arg("port"), nb::arg("password"));


}
