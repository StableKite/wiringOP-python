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
#include "wiringPi/mcp23x0817.h"
}

namespace nb = nanobind;

NB_MODULE(mcp23x0817, m) {
  m.doc() = "nanobind bindings for wiringPi/mcp23x0817.h";

  m.attr("MCP23X08_IODIR")=nb::cast((MCP23x08_IODIR));
  m.attr("MCP23X08_IPOL")=nb::cast((MCP23x08_IPOL));
  m.attr("MCP23X08_GPINTEN")=nb::cast((MCP23x08_GPINTEN));
  m.attr("MCP23X08_DEFVAL")=nb::cast((MCP23x08_DEFVAL));
  m.attr("MCP23X08_INTCON")=nb::cast((MCP23x08_INTCON));
  m.attr("MCP23X08_IOCON")=nb::cast((MCP23x08_IOCON));
  m.attr("MCP23X08_GPPU")=nb::cast((MCP23x08_GPPU));
  m.attr("MCP23X08_INTF")=nb::cast((MCP23x08_INTF));
  m.attr("MCP23X08_INTCAP")=nb::cast((MCP23x08_INTCAP));
  m.attr("MCP23X08_GPIO")=nb::cast((MCP23x08_GPIO));
  m.attr("MCP23X08_OLAT")=nb::cast((MCP23x08_OLAT));
  m.attr("MCP23X17_IODIRA")=nb::cast((MCP23x17_IODIRA));
  m.attr("MCP23X17_IPOLA")=nb::cast((MCP23x17_IPOLA));
  m.attr("MCP23X17_GPINTENA")=nb::cast((MCP23x17_GPINTENA));
  m.attr("MCP23X17_DEFVALA")=nb::cast((MCP23x17_DEFVALA));
  m.attr("MCP23X17_INTCONA")=nb::cast((MCP23x17_INTCONA));
  m.attr("MCP23X17_IOCON")=nb::cast((MCP23x17_IOCON));
  m.attr("MCP23X17_GPPUA")=nb::cast((MCP23x17_GPPUA));
  m.attr("MCP23X17_INTFA")=nb::cast((MCP23x17_INTFA));
  m.attr("MCP23X17_INTCAPA")=nb::cast((MCP23x17_INTCAPA));
  m.attr("MCP23X17_GPIO_A")=nb::cast((MCP23x17_GPIOA));
  m.attr("MCP23X17_OLATA")=nb::cast((MCP23x17_OLATA));
  m.attr("MCP23X17_IODIRB")=nb::cast((MCP23x17_IODIRB));
  m.attr("MCP23X17_IPOLB")=nb::cast((MCP23x17_IPOLB));
  m.attr("MCP23X17_GPINTENB")=nb::cast((MCP23x17_GPINTENB));
  m.attr("MCP23X17_DEFVALB")=nb::cast((MCP23x17_DEFVALB));
  m.attr("MCP23X17_INTCONB")=nb::cast((MCP23x17_INTCONB));
  m.attr("MCP23X17_IOCONB")=nb::cast((MCP23x17_IOCONB));
  m.attr("MCP23X17_GPPUB")=nb::cast((MCP23x17_GPPUB));
  m.attr("MCP23X17_INTFB")=nb::cast((MCP23x17_INTFB));
  m.attr("MCP23X17_INTCAPB")=nb::cast((MCP23x17_INTCAPB));
  m.attr("MCP23X17_GPIO_B")=nb::cast((MCP23x17_GPIOB));
  m.attr("MCP23X17_OLATB")=nb::cast((MCP23x17_OLATB));
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
