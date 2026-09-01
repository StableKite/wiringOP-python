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
#include "wiringPi/w25q64.h"
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
NB_MODULE(w25q64, m) {
  m.doc() = "nanobind bindings for wiringPi/w25q64.h";
  m.def("w25q64_begin", &W25Q64_begin, nb::arg("cs"));
  m.def("w25q64_read_status_reg1", &W25Q64_readStatusReg1);
  m.def("w25q64_read_status_reg2", &W25Q64_readStatusReg2);
  m.def("w25q64_read_manufacturer", []() { uint8_t b[3]={0}; W25Q64_readManufacturer(b); return nb::bytes(reinterpret_cast<char*>(b),3); });
  m.def("w25q64_read_unique_id", []() { uint8_t b[7]={0}; W25Q64_readUniqieID(b); return nb::bytes(reinterpret_cast<char*>(b),7); });
  m.def("w25q64_is_busy", &W25Q64_IsBusy);
  m.def("w25q64_power_down", &W25Q64_powerDown);
  m.def("w25q64_write_enable", &W25Q64_WriteEnable);
  m.def("w25q64_write_disable", &W25Q64_WriteDisable);
  m.def("w25q64_read", [](uint32_t addr,uint16_t n) { std::vector<uint8_t>b(n); uint16_t got=W25Q64_read(addr,b.data(),n); if(got>b.size()) got=(uint16_t)b.size(); return nb::bytes(reinterpret_cast<char*>(b.data()),got); }, nb::arg("addr"), nb::arg("n"));
  m.def("w25q64_fast_read", [](uint32_t addr,uint16_t n) { std::vector<uint8_t>b(n); uint16_t got=W25Q64_fastread(addr,b.data(),n); if(got>b.size()) got=(uint16_t)b.size(); return nb::bytes(reinterpret_cast<char*>(b.data()),got); }, nb::arg("addr"), nb::arg("n"));
  m.def("w25q64_erase_sector", &W25Q64_eraseSector, nb::arg("sect_no"), nb::arg("flgwait"));
  m.def("w25q64_erase64_block", &W25Q64_erase64Block, nb::arg("blk_no"), nb::arg("flgwait"));
  m.def("w25q64_erase32_block", &W25Q64_erase32Block, nb::arg("blk_no"), nb::arg("flgwait"));
  m.def("w25q64_erase_all", &W25Q64_eraseAll, nb::arg("flgwait"));
  m.def("w25q64_page_write", [](uint16_t sect_no,uint16_t inaddr,nb::handle data) { PyBufferGuard b(data,PyBUF_CONTIG_RO); if(b.view.len>255) throw nb::value_error("page write is limited to 255 bytes"); if((size_t)inaddr+(size_t)b.view.len>256) throw nb::value_error("write crosses a 256-byte page boundary"); return W25Q64_pageWrite(sect_no,inaddr,reinterpret_cast<uint8_t*>(b.view.buf),(uint8_t)b.view.len); }, nb::arg("sect_no"), nb::arg("inaddr"), nb::arg("data"));


}
