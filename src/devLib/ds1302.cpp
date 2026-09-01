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
#include "devLib/ds1302.h"
}

namespace nb = nanobind;

NB_MODULE(ds1302, m) {
  m.doc() = "nanobind bindings for devLib/ds1302.h";
  m.def("ds1302rtc_read", &ds1302rtcRead, nb::arg("reg"));
  m.def("ds1302rtc_write", &ds1302rtcWrite, nb::arg("reg"), nb::arg("data"));
  m.def("ds1302ram_read", &ds1302ramRead, nb::arg("addr"));
  m.def("ds1302ram_write", &ds1302ramWrite, nb::arg("addr"), nb::arg("data"));
  m.def("ds1302_clock_read", []() { int v[8]={0}; ds1302clockRead(v); nb::list out; for(int x:v) out.append(x); return nb::tuple(out); });
  m.def("ds1302_clock_write", [](nb::sequence seq) { if(nb::len(seq)!=8) throw nb::value_error("clock_data must contain 8 items"); int v[8]; for(size_t i=0;i<8;++i)v[i]=nb::cast<int>(seq[i]); ds1302clockWrite(v); }, nb::arg("clock_data"));
  m.def("ds1302trickle_charge", &ds1302trickleCharge, nb::arg("diodes"), nb::arg("resistors"));
  m.def("ds1302setup", &ds1302setup, nb::arg("clock_pin"), nb::arg("data_pin"), nb::arg("cs_pin"));


}
