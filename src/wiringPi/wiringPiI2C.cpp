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
#include "wiringPi/wiringPiI2C.h"
}

namespace nb = nanobind;

NB_MODULE(wiring_pi_i2c, m) {
  m.doc() = "nanobind bindings for wiringPi/wiringPiI2C.h";
  m.def("wiring_pi_i2c_read", &wiringPiI2CRead, nb::arg("fd"));
  m.def("wiring_pi_i2c_read_reg8", &wiringPiI2CReadReg8, nb::arg("fd"), nb::arg("reg"));
  m.def("wiring_pi_i2c_read_reg16", &wiringPiI2CReadReg16, nb::arg("fd"), nb::arg("reg"));
  m.def("wiring_pi_i2c_write", &wiringPiI2CWrite, nb::arg("fd"), nb::arg("data"));
  m.def("wiring_pi_i2c_write_reg8", &wiringPiI2CWriteReg8, nb::arg("fd"), nb::arg("reg"), nb::arg("data"));
  m.def("wiring_pi_i2c_write_reg16", &wiringPiI2CWriteReg16, nb::arg("fd"), nb::arg("reg"), nb::arg("data"));
  m.def("wiring_pi_i2c_setup_interface", &wiringPiI2CSetupInterface, nb::arg("device"), nb::arg("dev_id"));
  m.def("wiring_pi_i2c_setup", &wiringPiI2CSetup, nb::arg("dev_id"));


}
