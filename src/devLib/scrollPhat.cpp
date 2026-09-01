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
#include "devLib/scrollPhat.h"
}

namespace nb = nanobind;

NB_MODULE(scroll_phat, m) {
  m.doc() = "nanobind bindings for devLib/scrollPhat.h";
  m.def("scroll_phat_point", &scrollPhatPoint, nb::arg("x"), nb::arg("y"), nb::arg("colour"));
  m.def("scroll_phat_line", &scrollPhatLine, nb::arg("x0"), nb::arg("y0"), nb::arg("x1"), nb::arg("y1"), nb::arg("colour"));
  m.def("scroll_phat_line_to", &scrollPhatLineTo, nb::arg("x"), nb::arg("y"), nb::arg("colour"));
  m.def("scroll_phat_rectangle", &scrollPhatRectangle, nb::arg("x1"), nb::arg("y1"), nb::arg("x2"), nb::arg("y2"), nb::arg("colour"), nb::arg("filled"));
  m.def("scroll_phat_update", &scrollPhatUpdate);
  m.def("scroll_phat_clear", &scrollPhatClear);
  m.def("scroll_phat_putchar", &scrollPhatPutchar, nb::arg("c"));
  m.def("scroll_phat_puts", &scrollPhatPuts, nb::arg("str"));
  m.def("scroll_phat_printf", [](const char *message) { return scrollPhatPrintf("%s", message); }, nb::arg("message"));
  m.def("scroll_phat_print_speed", &scrollPhatPrintSpeed, nb::arg("cps10"));
  m.def("scroll_phat_intensity", &scrollPhatIntensity, nb::arg("percent"));
  m.def("scroll_phat_setup", &scrollPhatSetup);


}
