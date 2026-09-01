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
#include "wiringPi/oled.h"
}

namespace nb = nanobind;


struct PyBufferGuard {
    Py_buffer view{};
    bool active = false;
    PyBufferGuard(nb::handle obj, int flags) {
        if (PyObject_GetBuffer(obj.ptr(), &view, flags) != 0)
            throw nb::python_error();
        active = true;
    }
    ~PyBufferGuard() { if (active) PyBuffer_Release(&view); }
    PyBufferGuard(const PyBufferGuard &) = delete;
    PyBufferGuard &operator=(const PyBufferGuard &) = delete;
};
NB_MODULE(oled, m) {
  m.doc() = "nanobind bindings for wiringPi/oled.h";
  nb::module_::import_("wiringop.wiring_pi.font");
  auto cls_DisplayInfo = nb::class_<display_info>(m, "DisplayInfo").def(nb::init<>());
  cls_DisplayInfo.def_rw("address", &display_info::address);
  cls_DisplayInfo.def_rw("file", &display_info::file);
  cls_DisplayInfo.def_rw("font", &display_info::font);
  cls_DisplayInfo.def_prop_rw("buffer", [](display_info &self) { return nb::bytes(reinterpret_cast<const char *>(&self.buffer[0]), 1024); }, [](display_info &self, nb::bytes value) { if (nb::len(value) != 1024) throw nb::value_error("buffer must contain exactly 1024 bytes"); std::memcpy(&self.buffer[0], PyBytes_AS_STRING(value.ptr()), 1024); });
  auto cls_SizedArray = nb::class_<sized_array>(m, "SizedArray").def(nb::init<>());
  cls_SizedArray.def_rw("size", &sized_array::size);
  cls_SizedArray.def_prop_rw("array_address", [](sized_array &self) -> uintptr_t { return reinterpret_cast<uintptr_t>(self.array); }, [](sized_array &self, uintptr_t value) { self.array = reinterpret_cast<decltype(self.array)>(value); });
  m.def("oled_close", &oled_close, nb::arg("disp"));
  m.def("oled_open", [](display_info &disp,const char *filename) { std::vector<char>b(filename,filename+std::strlen(filename)+1); return oled_open(&disp,b.data()); }, nb::arg("disp"), nb::arg("filename"));
  m.def("oled_send", [](display_info &disp,nb::handle payload) { PyBufferGuard b(payload,PyBUF_CONTIG_RO); sized_array s{(int)b.view.len,reinterpret_cast<const uint8_t*>(b.view.buf)}; return oled_send(&disp,&s); }, nb::arg("disp"), nb::arg("payload"));
  m.def("oled_init", &oled_init, nb::arg("disp"));
  m.def("oled_send_buffer", &oled_send_buffer, nb::arg("disp"));
  m.def("oled_clear", &oled_clear, nb::arg("disp"));
  m.def("oled_putstr", [](display_info &disp,uint8_t line,const char *text) { std::vector<uint8_t>b(text,text+std::strlen(text)+1); oled_putstr(&disp,line,b.data()); }, nb::arg("disp"), nb::arg("line"), nb::arg("text"));
  m.def("oled_putpixel", &oled_putpixel, nb::arg("disp"), nb::arg("x"), nb::arg("y"), nb::arg("on"));
  m.def("oled_putstrto", [](display_info &disp,uint8_t x,uint8_t y,const char *text) { std::vector<char>b(text,text+std::strlen(text)+1); oled_putstrto(&disp,x,y,b.data()); }, nb::arg("disp"), nb::arg("x"), nb::arg("y"), nb::arg("text"));
  m.attr("display_config")=nb::bytes(reinterpret_cast<const char *>(&display_config[0]),29);
  m.attr("display_draw")=nb::bytes(reinterpret_cast<const char *>(&display_draw[0]),7);
  m.attr("OLED_I2C_ADDR")=nb::cast((OLED_I2C_ADDR));
  m.attr("OLED_CTRL_BYTE_CMD_SINGLE")=nb::cast((OLED_CTRL_BYTE_CMD_SINGLE));
  m.attr("OLED_CTRL_BYTE_CMD_STREAM")=nb::cast((OLED_CTRL_BYTE_CMD_STREAM));
  m.attr("OLED_CTRL_BYTE_DATA_STREAM")=nb::cast((OLED_CTRL_BYTE_DATA_STREAM));
  m.attr("OLED_CMD_SET_CONTRAST")=nb::cast((OLED_CMD_SET_CONTRAST));
  m.attr("OLED_CMD_DISPLAY_RAM")=nb::cast((OLED_CMD_DISPLAY_RAM));
  m.attr("OLED_CMD_DISPLAY_ALLON")=nb::cast((OLED_CMD_DISPLAY_ALLON));
  m.attr("OLED_CMD_DISPLAY_NORMAL")=nb::cast((OLED_CMD_DISPLAY_NORMAL));
  m.attr("OLED_CMD_DISPLAY_INVERTED")=nb::cast((OLED_CMD_DISPLAY_INVERTED));
  m.attr("OLED_CMD_DISPLAY_OFF")=nb::cast((OLED_CMD_DISPLAY_OFF));
  m.attr("OLED_CMD_DISPLAY_ON")=nb::cast((OLED_CMD_DISPLAY_ON));
  m.attr("OLED_CMD_SET_MEMORY_ADDR_MODE")=nb::cast((OLED_CMD_SET_MEMORY_ADDR_MODE));
  m.attr("OLED_CMD_SET_COLUMN_RANGE")=nb::cast((OLED_CMD_SET_COLUMN_RANGE));
  m.attr("OLED_CMD_SET_PAGE_RANGE")=nb::cast((OLED_CMD_SET_PAGE_RANGE));
  m.attr("OLED_CMD_SET_DISPLAY_START_LINE")=nb::cast((OLED_CMD_SET_DISPLAY_START_LINE));
  m.attr("OLED_CMD_SET_SEGMENT_REMAP")=nb::cast((OLED_CMD_SET_SEGMENT_REMAP));
  m.attr("OLED_CMD_SET_MUX_RATIO")=nb::cast((OLED_CMD_SET_MUX_RATIO));
  m.attr("OLED_CMD_SET_COM_SCAN_MODE")=nb::cast((OLED_CMD_SET_COM_SCAN_MODE));
  m.attr("OLED_CMD_SET_DISPLAY_OFFSET")=nb::cast((OLED_CMD_SET_DISPLAY_OFFSET));
  m.attr("OLED_CMD_SET_COM_PIN_MAP")=nb::cast((OLED_CMD_SET_COM_PIN_MAP));
  m.attr("OLED_CMD_NOP")=nb::cast((OLED_CMD_NOP));
  m.attr("OLED_CMD_SET_DISPLAY_CLK_DIV")=nb::cast((OLED_CMD_SET_DISPLAY_CLK_DIV));
  m.attr("OLED_CMD_SET_PRECHARGE")=nb::cast((OLED_CMD_SET_PRECHARGE));
  m.attr("OLED_CMD_SET_VCOMH_DESELCT")=nb::cast((OLED_CMD_SET_VCOMH_DESELCT));
  m.attr("OLED_CMD_SET_CHARGE_PUMP")=nb::cast((OLED_CMD_SET_CHARGE_PUMP));
  m.attr("OLED_SET_PAGE_ADDRESS")=nb::cast((OLED_SET_PAGE_ADDRESS));
}
