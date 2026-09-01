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
#include "wiringPiD/runRemote.h"
}

namespace nb = nanobind;

NB_MODULE(run_remote, m) {
  m.doc() = "nanobind bindings for wiringPiD/runRemote.h";
  m.def("run_remote_commands", &runRemoteCommands, nb::arg("fd"));
  m.def("get_no_local_pins", []() { return noLocalPins; });
  m.def("set_no_local_pins", [](decltype(noLocalPins) value) { noLocalPins=value; }, nb::arg("value"));

}
