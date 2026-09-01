# wiringop-nanobind

Полное Pythonic nanobind-покрытие `orangepi-xunlong/wiringOP`, закреплённого на ветке `next`, commit `a7921ca2f5c124203be10d3418db70a2e15f3c10`.

Проект рассматривает публичные upstream headers как контракт. Для каждого из 54 заголовков существуют зеркальные `src/**/*.cpp`, `tests/**/*.py`, `docs/**/*.md` и сгенерированный официальный `nanobind.stubgen` файл `stubs/**/*.pyi`.

Текущий Clang manifest содержит **260 функций, 19 структур, 207 полей, 26 header-visible variables и 664 macros**. В Python экспортируются 575 доказуемых value-macros и 2 bindable function-like macros.

## Структура

```text
extern/wiringOP/          git submodule на exact upstream commit
patches/wiringOP/         минимальные project overlays поверх upstream
src/<header>.cpp          nanobind binder
tests/<header>.py         зеркальный hardware-free acceptance test
docs/<header>.md          русская документация
stubs/<header>.pyi        результат official nanobind.stubgen 2.14.0
python/wiringop/          Python package + py.typed
support/mock_backend/     C ABI mock без GPIO hardware
tools/                    manifest, audits, PTY/QEMU tests, acceptance
```

## Python API

Функции и параметры используют `snake_case`, классы — `CapWords`, константы — `UPPER_SNAKE_CASE`. C output pointers возвращаются как Python values/tuples; byte buffers представлены buffer protocol/`bytes`; callbacks принимают Python callable. Raw pointer-поля низкоуровневых структур явно называются `*_address`.

Пример:

```python
from wiringop.wiring_pi import wiring_pi, wiring_pi_spi

wiring_pi.pin_mode(2, wiring_pi.OUTPUT)
wiring_pi.digital_write(2, wiring_pi.HIGH)

data = bytearray(b"\x9f\x00\x00\x00")
wiring_pi_spi.wiring_pi_spi_data_rw(0, data)
```

Расширенный UART API дополнительно предоставляет `SerialPort` и cancellable `serialContext*` операции. `SerialPort.close()` безопасно прерывает заблокированный Python `read()` без GIL deadlock; timeout-свойства поддерживают `None`.

## Production-сборка

```bash
git submodule update --init --recursive
python -m pip install .
```

`pyproject.toml` фиксирует build dependency `nanobind==2.14.0`. CMake автоматически находит установленный build-пакет nanobind, проверяет версию, готовит чистую копию закреплённого `wiringOP`, применяет project overlays и **по умолчанию собирает production backend**. Mock backend включается только явно через `-DWIRINGOP_USE_MOCK=ON`.

Для полностью offline CMake-сборки exact source tree можно передать непосредственно:

```bash
cmake -S . -B build/release \
  -DNB_ROOT=/path/to/nanobind-2.14.0 \
  -DWIRINGOP_USE_MOCK=OFF \
  -DCMAKE_BUILD_TYPE=Release
cmake --build build/release -j2
cmake --install build/release --prefix /desired/prefix
```

## Полный acceptance

Воспроизводимый hardware-free цикл запускается единым инструментом:

```bash
python tools/run_acceptance.py \
  --nb-root /path/to/exact/nanobind-2.14.0 \
  --nanobind-wheel /path/to/nanobind-2.14.0-py3-none-any.whl \
  --qemu-bundle /path/to/qemu-aarch64.tar.gz
```

Он проверяет exact dependency/upstream, повторно строит Clang manifest, выполняет layout/API/docs/ABI audits, собирает настоящий mock extension, импортирует 54 extension-модуля, запускает все pytest, генерирует 54 stubs официальным `nanobind.stubgen 2.14.0`, затем собирает production backend, выполняет production/PTY smoke tests, проверяет install-tree и при наличии bundle запускает AArch64 QEMU self-test.

Финальный проверенный прогон: **321/321 pytest**, **54/54 stubs**, **54/54 production imports**, install-tree **54 `.so` + 54 `.pyi` + `py.typed`**. Подробности сохранены в `ACCEPTANCE_RESULTS.md` и `ACCEPTANCE_LOG.txt`.

## Upstream PRs and project overlays

The warning cleanup and UART work are intentionally reviewable as two independent upstream changes:

- `upstream_prs/PR1-werror-cleanup.patch` — warning fixes required for strict `-Werror` builds;
- `upstream_prs/PR2-uart-standalone.patch` — enhanced cancellable/configurable UART API, based directly on the pinned upstream commit.

For this Python project the same changes are applied sequentially from `patches/wiringOP/`:

1. `0001-werror-cleanup.patch`;
2. `0002-wiringSerial-extended-UART.patch`.

The original `extern/wiringOP` remains clean at the pinned upstream commit.

## Release optimization policy

Release is the default CMake configuration. GCC/Clang Release builds use `-O3`, `NDEBUG`, and CMake IPO/LTO.
Generic hosts and cross builds deliberately receive no host-specific CPU flag. A native Linux/AArch64 build
whose device-tree model contains `Orange Pi 5` additionally receives `-mcpu=native`. This third optimization
layer is local to this project and is **not** part of either upstream PR.

`-Ofast` is intentionally not used because it may change floating-point/program semantics.

## Orange Pi 5 hardware validation

The delivery archive contains `hardware_validation/Run-OrangePi5-Validation.ps1`. From Windows it uploads a
fully offline payload to `root@192.168.1.6` and performs the final non-destructive build/runtime acceptance in
`/tmp`. The validator checks the board model/AArch64 architecture and the exact upstream source, then verifies:

- PR1 canonical upstream Makefile builds with `-Werror -O3 -flto -mcpu=native`;
- all 52 non-example C translation units compile with strict warnings-as-errors;
- PR2 builds with the same flags and passes the C UART PTY regression;
- the production nanobind build contains 54 modules and visibly uses `-O3`, LTO and `-mcpu=native`;
- production imports, Python UART PTY/deadlock regression, and installed package layout all pass.

The physical Orange Pi 5 run completed successfully with `ORANGEPI5_ACCEPTANCE_OK`: PR1 strict 52/52,
PR1+PR2 native `-Werror`, C/Python UART PTY, 54/54 production extensions/imports and the installed
54 `.so` + 54 `.pyi` + `py.typed` layout all passed with `-O3 -DNDEBUG -flto -mcpu=native`.
The full accepted identities and scope boundary are documented in `hardware_validation/LOCAL_VALIDATION_RESULTS.md`.

## Upstream linker gaps

Текущий wiringOP объявляет, но не определяет `digitalRead8`, `digitalWrite8`, `wiringPiSetupPiFace`, `wiringPiSetupPiFaceForGpioProg`; Python сохраняет эти имена и выдаёт `NotImplementedError`. `getResponce` — upstream typo, совместимо перенаправленный на существующий `getResponse` как `get_response_legacy`.

## ARM64

Помимо базового loader self-test, финальный pre-hardware gate компилирует и LTO-линкует реальный код `wiringPi` как AArch64 PIE и запускает его под bundled qemu-aarch64. Проверенный результат: `WIRINGOP_AARCH64_QEMU_OK version=2.46`. Физический Orange Pi 5 build/link/load/runtime gate также пройден (`ORANGEPI5_ACCEPTANCE_OK`); электрическое переключение реальных GPIO-линий намеренно не выполнялось.

## Лицензия

LGPL-3.0-or-later.
