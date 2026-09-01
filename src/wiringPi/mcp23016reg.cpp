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
#include "wiringPi/mcp23016reg.h"
}

namespace nb = nanobind;

NB_MODULE(mcp23016reg, m) {
  m.doc() = "nanobind bindings for wiringPi/mcp23016reg.h";

  m.attr("MCP23016_GP0")=nb::cast((MCP23016_GP0));
  m.attr("MCP23016_GP1")=nb::cast((MCP23016_GP1));
  m.attr("MCP23016_OLAT0")=nb::cast((MCP23016_OLAT0));
  m.attr("MCP23016_OLAT1")=nb::cast((MCP23016_OLAT1));
  m.attr("MCP23016_IPOL0")=nb::cast((MCP23016_IPOL0));
  m.attr("MCP23016_IPOL1")=nb::cast((MCP23016_IPOL1));
  m.attr("MCP23016_IODIR0")=nb::cast((MCP23016_IODIR0));
  m.attr("MCP23016_IODIR1")=nb::cast((MCP23016_IODIR1));
  m.attr("MCP23016_INTCAP0")=nb::cast((MCP23016_INTCAP0));
  m.attr("MCP23016_INTCAP1")=nb::cast((MCP23016_INTCAP1));
  m.attr("MCP23016_IOCON0")=nb::cast((MCP23016_IOCON0));
  m.attr("MCP23016_IOCON1")=nb::cast((MCP23016_IOCON1));
  m.attr("IOCON_IARES")=nb::cast((IOCON_IARES));
  m.attr("IOCON_INIT")=nb::cast((IOCON_INIT));
}
