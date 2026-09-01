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
#include "wiringPi/softTone.h"
}

namespace nb = nanobind;

NB_MODULE(soft_tone, m) {
  m.doc() = "nanobind bindings for wiringPi/softTone.h";
  m.def("soft_tone_create", &softToneCreate, nb::arg("pin"));
  m.def("soft_tone_stop", &softToneStop, nb::arg("pin"));
  m.def("soft_tone_write", &softToneWrite, nb::arg("pin"), nb::arg("freq"));


}
