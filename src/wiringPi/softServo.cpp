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
#include "wiringPi/softServo.h"
}

namespace nb = nanobind;

NB_MODULE(soft_servo, m) {
  m.doc() = "nanobind bindings for wiringPi/softServo.h";
  m.def("soft_servo_write", &softServoWrite, nb::arg("pin"), nb::arg("value"));
  m.def("soft_servo_setup", &softServoSetup, nb::arg("p0"), nb::arg("p1"), nb::arg("p2"), nb::arg("p3"), nb::arg("p4"), nb::arg("p5"), nb::arg("p6"), nb::arg("p7"));


}
