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
#include "wiringPi/font.h"
}

namespace nb = nanobind;

NB_MODULE(font, m) {
  m.doc() = "nanobind bindings for wiringPi/font.h";
  auto cls_FontInfo = nb::class_<font_info>(m, "FontInfo").def(nb::init<>());
  cls_FontInfo.def_rw("width", &font_info::width);
  cls_FontInfo.def_rw("height", &font_info::height);
  cls_FontInfo.def_rw("spacing", &font_info::spacing);
  cls_FontInfo.def_rw("offset", &font_info::offset);
  cls_FontInfo.def_prop_rw("data_address", [](font_info &self) -> uintptr_t { return reinterpret_cast<uintptr_t>(self.data); }, [](font_info &self, uintptr_t value) { self.data = reinterpret_cast<decltype(self.data)>(value); });
  m.attr("font1_data")=nb::bytes(reinterpret_cast<const char *>(&font1_data[0]),1280);
  m.attr("font2_data")=nb::bytes(reinterpret_cast<const char *>(&font2_data[0]),570);
  m.attr("font3_data")=nb::bytes(reinterpret_cast<const char *>(&font3_data[0]),7125);
  m.def("get_font1", []() { return font1; });
  m.def("set_font1", [](font_info value) { font1=value; }, nb::arg("value"));
  m.def("get_font2", []() { return font2; });
  m.def("set_font2", [](font_info value) { font2=value; }, nb::arg("value"));
  m.def("get_font3", []() { return font3; });
  m.def("set_font3", [](font_info value) { font3=value; }, nb::arg("value"));

}
