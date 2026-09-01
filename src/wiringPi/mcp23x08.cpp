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
#include "wiringPi/mcp23x08.h"
}

namespace nb = nanobind;

NB_MODULE(mcp23x08, m) {
  m.doc() = "nanobind bindings for wiringPi/mcp23x08.h";

  m.attr("IODIRA")=nb::cast((IODIRA));
  m.attr("IPOLA")=nb::cast((IPOLA));
  m.attr("GPINTENA")=nb::cast((GPINTENA));
  m.attr("DEFVALA")=nb::cast((DEFVALA));
  m.attr("INTCONA")=nb::cast((INTCONA));
  m.attr("IOCON")=nb::cast((IOCON));
  m.attr("GPPUA")=nb::cast((GPPUA));
  m.attr("INTFA")=nb::cast((INTFA));
  m.attr("INTCAPA")=nb::cast((INTCAPA));
  m.attr("GPIO_A")=nb::cast((GPIOA));
  m.attr("OLATA")=nb::cast((OLATA));
  m.attr("IODIRB")=nb::cast((IODIRB));
  m.attr("IPOLB")=nb::cast((IPOLB));
  m.attr("GPINTENB")=nb::cast((GPINTENB));
  m.attr("DEFVALB")=nb::cast((DEFVALB));
  m.attr("INTCONB")=nb::cast((INTCONB));
  m.attr("IOCONB")=nb::cast((IOCONB));
  m.attr("GPPUB")=nb::cast((GPPUB));
  m.attr("INTFB")=nb::cast((INTFB));
  m.attr("INTCAPB")=nb::cast((INTCAPB));
  m.attr("GPIO_B")=nb::cast((GPIOB));
  m.attr("OLATB")=nb::cast((OLATB));
  m.attr("IOCON_UNUSED")=nb::cast((IOCON_UNUSED));
  m.attr("IOCON_INTPOL")=nb::cast((IOCON_INTPOL));
  m.attr("IOCON_ODR")=nb::cast((IOCON_ODR));
  m.attr("IOCON_HAEN")=nb::cast((IOCON_HAEN));
  m.attr("IOCON_DISSLW")=nb::cast((IOCON_DISSLW));
  m.attr("IOCON_SEQOP")=nb::cast((IOCON_SEQOP));
  m.attr("IOCON_MIRROR")=nb::cast((IOCON_MIRROR));
  m.attr("IOCON_BANK_MODE")=nb::cast((IOCON_BANK_MODE));
  m.attr("IOCON_INIT")=nb::cast((IOCON_INIT));
  m.attr("CMD_WRITE")=nb::cast((CMD_WRITE));
  m.attr("CMD_READ")=nb::cast((CMD_READ));
}
