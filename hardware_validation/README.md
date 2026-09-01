# Orange Pi 5 hardware validation

`Run-OrangePi5-Validation.ps1` uploads the bundled offline payload to
`root@192.168.1.6` by default and runs a non-destructive build/PTY acceptance in
`/tmp`.

The remote validator verifies:

- device-tree model contains `Orange Pi 5` and architecture is AArch64;
- PR1 warning cleanup builds the upstream wiringOP libraries and `gpio` with
  `-Werror -O3 -flto -mcpu=native`;
- all 52 non-example C translation units compile with strict warnings-as-errors;
- PR2 UART integration builds with the same strict flags and passes the C PTY
  cancellation/ownership regression;
- the production nanobind package builds 54 extension modules using the local
  optimization layer (`-O3`, `NDEBUG`, IPO/LTO, `-mcpu=native` on Orange Pi 5);
- 54 production modules import, the Python UART PTY/deadlock test passes, and
  the installed tree contains 54 `.so`, 54 `.pyi`, and `py.typed`.

No GPIO registers are exercised by this validation. It tests compilation,
linking, import/runtime loading, and UART behavior via a pseudo-terminal.

## Prerequisites on the Orange Pi

The payload is offline, but the board must already have a native build toolchain and development headers:
`gcc`, `g++`, `make`, `cmake`, `git`, `patch`, `python3`, `python3-config`, the matching Python development headers, and linkable `crypt.h`/`libcrypt` development files.

The PowerShell runner verifies the SHA-256 of `wiringop_orangepi5_payload.tar.gz` before uploading it. The Linux validator also verifies SHA-256 for all 213 tracked files of the pinned upstream source before applying either PR, and verifies every file in the bundled exact nanobind 2.14.0 dependency tree before the production build.

A `results.tar.gz` archive is produced on both success and failure. On failure the PowerShell runner keeps the live SSH log and attempts to download the partial result archive before removing the temporary remote workspace.
