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
#include "wiringPi/softPwm.h"
}

namespace nb = nanobind;

NB_MODULE(soft_pwm, m) {
  m.doc() = "nanobind bindings for wiringPi/softPwm.h";
  m.def("soft_pwm_create", &softPwmCreate, nb::arg("pin"), nb::arg("value"), nb::arg("range"));
  m.def("soft_pwm_write", &softPwmWrite, nb::arg("pin"), nb::arg("value"));
  m.def("soft_pwm_stop", &softPwmStop, nb::arg("pin"));


}
