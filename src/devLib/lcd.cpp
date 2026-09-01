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
#include "devLib/lcd.h"
}

namespace nb = nanobind;

NB_MODULE(lcd, m) {
  m.doc() = "nanobind bindings for devLib/lcd.h";
  m.def("lcd_home", &lcdHome, nb::arg("fd"));
  m.def("lcd_clear", &lcdClear, nb::arg("fd"));
  m.def("lcd_display", &lcdDisplay, nb::arg("fd"), nb::arg("state"));
  m.def("lcd_cursor", &lcdCursor, nb::arg("fd"), nb::arg("state"));
  m.def("lcd_cursor_blink", &lcdCursorBlink, nb::arg("fd"), nb::arg("state"));
  m.def("lcd_send_command", &lcdSendCommand, nb::arg("fd"), nb::arg("command"));
  m.def("lcd_position", &lcdPosition, nb::arg("fd"), nb::arg("x"), nb::arg("y"));
  m.def("lcd_char_def", [](int fd,int index,nb::bytes data) { if(nb::len(data)!=8) throw nb::value_error("data must contain exactly 8 bytes"); unsigned char v[8]; std::memcpy(v,PyBytes_AS_STRING(data.ptr()),8); lcdCharDef(fd,index,v); }, nb::arg("fd"), nb::arg("index"), nb::arg("data"));
  m.def("lcd_putchar", &lcdPutchar, nb::arg("fd"), nb::arg("data"));
  m.def("lcd_puts", &lcdPuts, nb::arg("fd"), nb::arg("string"));
  m.def("lcd_printf", [](const int fd, const char *message) { return lcdPrintf(fd, "%s", message); }, nb::arg("fd"), nb::arg("message"));
  m.def("lcd_init", &lcdInit, nb::arg("rows"), nb::arg("cols"), nb::arg("bits"), nb::arg("rs"), nb::arg("strb"), nb::arg("d0"), nb::arg("d1"), nb::arg("d2"), nb::arg("d3"), nb::arg("d4"), nb::arg("d5"), nb::arg("d6"), nb::arg("d7"));

  m.attr("MAX_LCDS")=nb::cast((MAX_LCDS));
}
