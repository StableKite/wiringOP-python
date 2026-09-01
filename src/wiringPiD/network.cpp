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
#include "wiringPiD/network.h"
}

namespace nb = nanobind;

NB_MODULE(network, m) {
  m.doc() = "nanobind bindings for wiringPiD/network.h";
  m.def("get_client_ip", &getClientIP, nb::rv_policy::reference);
  m.def("get_response_legacy", [](int client_fd) { return getResponse(client_fd); }, nb::arg("client_fd"));
  m.def("setup_server", &setupServer, nb::arg("server_port"));
  m.def("send_greeting", &sendGreeting, nb::arg("client_fd"));
  m.def("send_challenge", &sendChallenge, nb::arg("client_fd"));
  m.def("get_response", &getResponse, nb::arg("client_fd"));
  m.def("password_match", &passwordMatch, nb::arg("password"));
  m.def("close_server", &closeServer, nb::arg("client_fd"));


}
