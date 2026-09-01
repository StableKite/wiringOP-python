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
#include "devLib/piNes.h"
}

namespace nb = nanobind;

NB_MODULE(pi_nes, m) {
  m.doc() = "nanobind bindings for devLib/piNes.h";
  m.def("setup_nes_joystick", &setupNesJoystick, nb::arg("d_pin"), nb::arg("c_pin"), nb::arg("l_pin"));
  m.def("read_nes_joystick", &readNesJoystick, nb::arg("joystick"));

  m.attr("MAX_NES_JOYSTICKS")=nb::cast((MAX_NES_JOYSTICKS));
  m.attr("NES_RIGHT")=nb::cast((NES_RIGHT));
  m.attr("NES_LEFT")=nb::cast((NES_LEFT));
  m.attr("NES_DOWN")=nb::cast((NES_DOWN));
  m.attr("NES_UP")=nb::cast((NES_UP));
  m.attr("NES_START")=nb::cast((NES_START));
  m.attr("NES_SELECT")=nb::cast((NES_SELECT));
  m.attr("NES_B")=nb::cast((NES_B));
  m.attr("NES_A")=nb::cast((NES_A));
}
