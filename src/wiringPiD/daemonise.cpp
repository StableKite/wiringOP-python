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
#include "wiringPiD/daemonise.h"
}

namespace nb = nanobind;

NB_MODULE(daemonise, m) {
  m.doc() = "nanobind bindings for wiringPiD/daemonise.h";
  m.def("daemonise", &daemonise, nb::arg("pid_file"));


}
