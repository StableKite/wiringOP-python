# Финальный acceptance checklist

Проект считается завершённым только если все применимые пункты ниже проходят в одной сохранённой версии дерева.

## Upstream/layout

- [x] `extern/wiringOP` — gitlink/submodule на exact commit `a7921ca2f5c124203be10d3418db70a2e15f3c10`.
- [x] upstream clean.
- [x] ровно 54 non-example headers обнаруживаются generator/audit.
- [x] каждый header имеет mirrored public binder/test/doc/stub target.
- [x] нет `tests/**/test_*.py`.
- [x] публичный package/layout зеркален и проходит `audit_layout.py`.

## Manifest completeness

- [x] Clang AST functions coverage.
- [x] correct pointer return types.
- [x] callbacks/variadic functions не потеряны.
- [x] named + anonymous typedef structs.
- [x] every struct field.
- [x] enums (в текущем публичном manifest: 0).
- [x] globals/header-visible objects.
- [x] object-like macros classified by compile check.
- [x] bindable function-like macros.
- [x] C-only macros явно остаются записанными в manifest и не выдаются за Python values.

## Backend

- [x] production C source set compiles.
- [x] `nm` symbol audit.
- [x] only known upstream missing symbols are allowlisted.
- [x] mock backend compiles.
- [x] mock relocatable link catches duplicate symbols.
- [x] mock implements every runtime-testable C ABI symbol.

## Real nanobind build

- [x] **real nanobind 2.14.0** headers/runtime, not shim.
- [x] mock extension builds: 54/54 modules.
- [x] compiled package imports: 57/57 modules.
- [x] all mirrored pytest files run: 321/321 tests passed.
- [x] mapped runtime-safe functions реально вызываются mock tests.
- [x] buffers/output pointers/callbacks/structs/globals/constants имеют semantic assertions.
- [x] Python `SerialPort` PTY cancellation/close regression проходит без GIL deadlock.

## Stubgen

- [x] run official `nanobind.stubgen 2.14.0`.
- [x] generated stubs physically mirror 54 public `.cpp` modules.
- [x] all function names/signatures present.
- [x] no accidental `arg0`, `arg1` where meaningful names exist.
- [x] all classes/fields present.
- [x] globals/accessors present.
- [x] all Python-exported constants present.
- [x] `py.typed` установлен вместе со stubs.

## Docs

- [x] 54 mirrored Russian docs.
- [x] нет boilerplate-only docs.
- [x] каждый manifest C/Python symbol отражён documentation audit.
- [x] adaptations and limitations documented.

## Production build / install

- [x] production extensions build against real prepared wiringOP C backend: 54/54.
- [x] smoke import не трогает GPIO hardware: 57/57.
- [x] no unexpected undefined linker symbols.
- [x] default CMake package configuration выбирает production backend, auto-discovers exact nanobind и auto-prepares overlays.
- [x] clean install-tree содержит 54 `.so`, 54 `.pyi`, `py.typed` и не содержит build-time `__pycache__`/`.pyc`.

## ARM64

- [x] QEMU bundle SHA-256 проверен и self-test проходит.
- [x] cross-compiled AArch64 Python extension smoke — N/A: в acceptance environment нет AArch64 Python headers/toolchain; условный пункт не подменяется host build.
- [x] реальное RK3588 GPIO hardware testing под QEMU не заявляется.

## Delivery

- [x] git status clean.
- [x] final commit created.
- [x] acceptance log saved in repository/artifact.
- [x] final project archive created and SHA-256 recorded.
