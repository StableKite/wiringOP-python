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
#include "wiringPiD/drcNetCmd.h"
}

namespace nb = nanobind;

NB_MODULE(drc_net_cmd, m) {
  m.doc() = "nanobind bindings for wiringPiD/drcNetCmd.h";
  auto cls_DrcNetComStruct = nb::class_<drcNetComStruct>(m, "DrcNetComStruct").def(nb::init<>());
  cls_DrcNetComStruct.def_rw("pin", &drcNetComStruct::pin);
  cls_DrcNetComStruct.def_rw("cmd", &drcNetComStruct::cmd);
  cls_DrcNetComStruct.def_rw("data", &drcNetComStruct::data);

  m.attr("DEFAULT_SERVER_PORT")=nb::cast((DEFAULT_SERVER_PORT));
  m.attr("DRCN_PIN_MODE")=nb::cast((DRCN_PIN_MODE));
  m.attr("DRCN_PULL_UP_DN")=nb::cast((DRCN_PULL_UP_DN));
  m.attr("DRCN_DIGITAL_WRITE")=nb::cast((DRCN_DIGITAL_WRITE));
  m.attr("DRCN_DIGITAL_WRITE8")=nb::cast((DRCN_DIGITAL_WRITE8));
  m.attr("DRCN_ANALOG_WRITE")=nb::cast((DRCN_ANALOG_WRITE));
  m.attr("DRCN_PWM_WRITE")=nb::cast((DRCN_PWM_WRITE));
  m.attr("DRCN_DIGITAL_READ")=nb::cast((DRCN_DIGITAL_READ));
  m.attr("DRCN_DIGITAL_READ8")=nb::cast((DRCN_DIGITAL_READ8));
  m.attr("DRCN_ANALOG_READ")=nb::cast((DRCN_ANALOG_READ));
}
