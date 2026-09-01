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
#include "devLib/piFace.h"
}

namespace nb = nanobind;

NB_MODULE(pi_face, m) {
  m.doc() = "nanobind bindings for devLib/piFace.h";
  m.def("pi_face_setup", &piFaceSetup, nb::arg("pin_base"));


}
