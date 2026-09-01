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
#include "wiringPi/mcp3422.h"
}

namespace nb = nanobind;

NB_MODULE(mcp3422, m) {
  m.doc() = "nanobind bindings for wiringPi/mcp3422.h";
  m.def("mcp3422_setup", &mcp3422Setup, nb::arg("pin_base"), nb::arg("i2c_address"), nb::arg("sample_rate"), nb::arg("gain"));

  m.attr("MCP3422_SR_240")=nb::cast((MCP3422_SR_240));
  m.attr("MCP3422_SR_60")=nb::cast((MCP3422_SR_60));
  m.attr("MCP3422_SR_15")=nb::cast((MCP3422_SR_15));
  m.attr("MCP3422_SR_3_75")=nb::cast((MCP3422_SR_3_75));
  m.attr("MCP3422_GAIN_1")=nb::cast((MCP3422_GAIN_1));
  m.attr("MCP3422_GAIN_2")=nb::cast((MCP3422_GAIN_2));
  m.attr("MCP3422_GAIN_4")=nb::cast((MCP3422_GAIN_4));
  m.attr("MCP3422_GAIN_8")=nb::cast((MCP3422_GAIN_8));
}
