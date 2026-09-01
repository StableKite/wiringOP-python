# Final Orange Pi 5 hardware acceptance

Status: **PASS — `ORANGEPI5_ACCEPTANCE_OK`**

This directory is the canonical v1.0.3 source/delivery plus the evidence captured from the successful physical Orange Pi 5 run on 2026-09-01. The accepted source tree, PR patches, integration tree, offline payload, and validator are unchanged from v1.0.3; only this evidence layer and final manifests were added after the run.

## Accepted identities

- root project: `08df7fed1eb59c67f769ee80ffdc3b8e1cdfa6ef`
- wiringOP pinned base: `a7921ca2f5c124203be10d3418db70a2e15f3c10`
- PR1 warning / strict-`-Werror` cleanup: `c6d9ecbcafe2a6eb4c2cb34be8a8ffb7b16537d3`
- PR2 standalone UART change based directly on the pinned base: `2f8aea5af3a94573ffb887816ed0ba5acd462cae`
- integration PR1 + PR2: `3a666f78d8529b70209a4e3d6e6e2f47047ad498`
- nanobind: `2.14.0` / `86e5626728fc282637a6c338597120913dded1bb`
- robin-map: `4ec1bf19c6a96125ea22062f38c2cf5b958e448e`
- offline payload SHA-256: `738c528b315d48f1ab8b36e8e699a3193b5e5fa64bddda1040566cc2b9d9d8d9`
- original accepted v1.0.3 ZIP SHA-256: `981b6b3cea2624fe608fa1c36dd3f622f1e3e4cee7005ad09fe2561b74ec95d9`

## Physical board / toolchain

- model: `Orange Pi 5`
- architecture: `aarch64`
- GCC/G++: Ubuntu `13.3.0`
- CMake: `3.28.3`
- Python: `3.12.3`
- matching Python include tree and linkable `libcrypt` development files verified
- exact bundled nanobind tree SHA-256 verified
- all 213 tracked files of pinned upstream wiringOP verified before patching

## Hardware-run gates that passed

- `PR1_NATIVE_WERROR_BUILD_OK`
- `PR1_STRICT_TRANSLATION_UNITS_OK 52/52`
- `PR1_PR2_NATIVE_WERROR_BUILD_OK`
- `WIRING_SERIAL_EXT_PTY_OK`
- CMake detected the physical Orange Pi 5 and enabled `-mcpu=native`
- production build used `-O3 -DNDEBUG`, IPO/LTO, and `-mcpu=native`
- `PRODUCTION_EXTENSIONS_OK 54/54`
- `PRODUCTION_IMPORT_OK 54/54`
- `PYTHON_SERIAL_PROD_PTY_OK`
- install tree: 54 `.so`, 54 `.pyi`, and `py.typed`
- `INSTALL_IMPORT_OK 54/54`
- final marker: `ORANGEPI5_ACCEPTANCE_OK`

The complete UTF-16 Windows live log, a UTF-8 conversion, the downloaded `results.tar.gz`, its extracted result files, and the PowerShell console transcript are under `hardware_evidence/`.

A scan of the complete decoded hardware log found no `error:`, `fatal:`, `FAILED`, `Traceback`, `Exception`, `undefined reference`, `No such file`, or `not found` failure markers.

## Scope boundary

This is a physical Orange Pi 5 native build/link/load/runtime acceptance and UART pseudo-terminal regression. The validator is intentionally non-destructive and **does not toggle or electrically test real GPIO pins/registers**. Electrical GPIO behavior therefore remains outside this acceptance claim.
