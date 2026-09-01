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
#include "wiringPi/wiringPiSPI.h"
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
NB_MODULE(wiring_pi_spi, m) {
  m.doc() = "nanobind bindings for wiringPi/wiringPiSPI.h";
  m.def("wiring_pi_spi_get_fd", &wiringPiSPIGetFd, nb::arg("channel"));
  m.def("wiring_pi_spi_data_rw", [](int channel,nb::handle data) { PyBufferGuard b(data,PyBUF_WRITABLE|PyBUF_C_CONTIGUOUS); return wiringPiSPIDataRW(channel,reinterpret_cast<unsigned char*>(b.view.buf),(int)b.view.len); }, nb::arg("channel"), nb::arg("data"));
  m.def("wiring_pi_spi_setup_mode", &wiringPiSPISetupMode, nb::arg("channel"), nb::arg("port"), nb::arg("speed"), nb::arg("mode"));
  m.def("wiring_pi_spi_setup", &wiringPiSPISetup, nb::arg("channel"), nb::arg("speed"));


}
