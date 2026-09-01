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
#include "wiringPi/ads1115.h"
}

namespace nb = nanobind;

NB_MODULE(ads1115, m) {
  m.doc() = "nanobind bindings for wiringPi/ads1115.h";
  m.def("ads1115_setup", &ads1115Setup, nb::arg("pin_base"), nb::arg("i2c_address"));

  m.attr("ADS1115_GAIN_6")=nb::cast((ADS1115_GAIN_6));
  m.attr("ADS1115_GAIN_4")=nb::cast((ADS1115_GAIN_4));
  m.attr("ADS1115_GAIN_2")=nb::cast((ADS1115_GAIN_2));
  m.attr("ADS1115_GAIN_1")=nb::cast((ADS1115_GAIN_1));
  m.attr("ADS1115_GAIN_HALF")=nb::cast((ADS1115_GAIN_HALF));
  m.attr("ADS1115_GAIN_QUARTER")=nb::cast((ADS1115_GAIN_QUARTER));
  m.attr("ADS1115_DR_8")=nb::cast((ADS1115_DR_8));
  m.attr("ADS1115_DR_16")=nb::cast((ADS1115_DR_16));
  m.attr("ADS1115_DR_32")=nb::cast((ADS1115_DR_32));
  m.attr("ADS1115_DR_64")=nb::cast((ADS1115_DR_64));
  m.attr("ADS1115_DR_128")=nb::cast((ADS1115_DR_128));
  m.attr("ADS1115_DR_250")=nb::cast((ADS1115_DR_250));
  m.attr("ADS1115_DR_475")=nb::cast((ADS1115_DR_475));
  m.attr("ADS1115_DR_860")=nb::cast((ADS1115_DR_860));
}
