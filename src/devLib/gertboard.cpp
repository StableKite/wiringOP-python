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
#include "devLib/gertboard.h"
}

namespace nb = nanobind;

NB_MODULE(gertboard, m) {
  m.doc() = "nanobind bindings for devLib/gertboard.h";
  m.def("gertboard_analog_write", &gertboardAnalogWrite, nb::arg("chan"), nb::arg("value"));
  m.def("gertboard_analog_read", &gertboardAnalogRead, nb::arg("chan"));
  m.def("gertboard_spi_setup", &gertboardSPISetup);
  m.def("gertboard_analog_setup", &gertboardAnalogSetup, nb::arg("pin_base"));


}
