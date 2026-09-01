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
#include "devLib/piGlow.h"
}

namespace nb = nanobind;

NB_MODULE(pi_glow, m) {
  m.doc() = "nanobind bindings for devLib/piGlow.h";
  m.def("pi_glow1", &piGlow1, nb::arg("leg"), nb::arg("ring"), nb::arg("intensity"));
  m.def("pi_glow_leg", &piGlowLeg, nb::arg("leg"), nb::arg("intensity"));
  m.def("pi_glow_ring", &piGlowRing, nb::arg("ring"), nb::arg("intensity"));
  m.def("pi_glow_setup", &piGlowSetup, nb::arg("clear"));

  m.attr("PIGLOW_RED")=nb::cast((PIGLOW_RED));
  m.attr("PIGLOW_ORANGE")=nb::cast((PIGLOW_ORANGE));
  m.attr("PIGLOW_YELLOW")=nb::cast((PIGLOW_YELLOW));
  m.attr("PIGLOW_GREEN")=nb::cast((PIGLOW_GREEN));
  m.attr("PIGLOW_BLUE")=nb::cast((PIGLOW_BLUE));
  m.attr("PIGLOW_WHITE")=nb::cast((PIGLOW_WHITE));
}
