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
#include "devLib/lcd128x64.h"
}

namespace nb = nanobind;

NB_MODULE(lcd128x64, m) {
  m.doc() = "nanobind bindings for devLib/lcd128x64.h";
  m.def("lcd128x64set_origin", &lcd128x64setOrigin, nb::arg("x"), nb::arg("y"));
  m.def("lcd128x64set_orientation", &lcd128x64setOrientation, nb::arg("orientation"));
  m.def("lcd128x64orient_coordinates", []() { int x=0; int y=0; lcd128x64orientCoordinates(&x, &y); return nb::make_tuple(x, y); });
  m.def("lcd128x64_get_screen_size", []() { int x=0,y=0; lcd128x64getScreenSize(&x,&y); return nb::make_tuple(x,y); });
  m.def("lcd128x64point", &lcd128x64point, nb::arg("x"), nb::arg("y"), nb::arg("colour"));
  m.def("lcd128x64line", &lcd128x64line, nb::arg("x0"), nb::arg("y0"), nb::arg("x1"), nb::arg("y1"), nb::arg("colour"));
  m.def("lcd128x64line_to", &lcd128x64lineTo, nb::arg("x"), nb::arg("y"), nb::arg("colour"));
  m.def("lcd128x64rectangle", &lcd128x64rectangle, nb::arg("x1"), nb::arg("y1"), nb::arg("x2"), nb::arg("y2"), nb::arg("colour"), nb::arg("filled"));
  m.def("lcd128x64circle", &lcd128x64circle, nb::arg("x"), nb::arg("y"), nb::arg("r"), nb::arg("colour"), nb::arg("filled"));
  m.def("lcd128x64ellipse", &lcd128x64ellipse, nb::arg("cx"), nb::arg("cy"), nb::arg("x_radius"), nb::arg("y_radius"), nb::arg("colour"), nb::arg("filled"));
  m.def("lcd128x64putchar", &lcd128x64putchar, nb::arg("x"), nb::arg("y"), nb::arg("c"), nb::arg("bg_col"), nb::arg("fg_col"));
  m.def("lcd128x64puts", &lcd128x64puts, nb::arg("x"), nb::arg("y"), nb::arg("str"), nb::arg("bg_col"), nb::arg("fg_col"));
  m.def("lcd128x64update", &lcd128x64update);
  m.def("lcd128x64clear", &lcd128x64clear, nb::arg("colour"));
  m.def("lcd128x64setup", &lcd128x64setup);


}
