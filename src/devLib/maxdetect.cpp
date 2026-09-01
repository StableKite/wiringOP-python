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
#include "devLib/maxdetect.h"
}

namespace nb = nanobind;

NB_MODULE(maxdetect, m) {
  m.doc() = "nanobind bindings for devLib/maxdetect.h";
  m.def("max_detect_read", [](int pin) { unsigned char b[4]={0}; int st=maxDetectRead(pin,b); return nb::make_tuple(st, nb::bytes(reinterpret_cast<char*>(b),4)); }, nb::arg("pin"));
  m.def("read_rht03", [](int pin) { int temp=0,rh=0; int st=readRHT03(pin,&temp,&rh); return nb::make_tuple(st,temp,rh); }, nb::arg("pin"));


}
