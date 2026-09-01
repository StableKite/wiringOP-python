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
#include "wiringPi/wpiExtensions.h"
}

namespace nb = nanobind;

NB_MODULE(wpi_extensions, m) {
  m.doc() = "nanobind bindings for wiringPi/wpiExtensions.h";
  m.def("load_wpi_extension", [](const char *progName, const char *extensionData, int verbose) { std::vector<char> progName_buf(progName,progName+std::strlen(progName)+1); std::vector<char> extensionData_buf(extensionData,extensionData+std::strlen(extensionData)+1); return loadWPiExtension(progName_buf.data(), extensionData_buf.data(), verbose); }, nb::arg("prog_name"), nb::arg("extension_data"), nb::arg("verbose"));


}
