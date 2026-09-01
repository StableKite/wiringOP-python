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
#include "version.h"
}

namespace nb = nanobind;

NB_MODULE(version, m) {
  m.doc() = "nanobind bindings for version.h";

  m.attr("VERSION")=nb::cast((VERSION));
  m.attr("VERSION_MAJOR")=nb::cast((VERSION_MAJOR));
  m.attr("VERSION_MINOR")=nb::cast((VERSION_MINOR));
}
