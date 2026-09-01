# Финальные результаты acceptance

Финальный воспроизводимый прогон выполнен после последних packaging-изменений единым `tools/run_acceptance.py` и завершился `ACCEPTANCE_OK`.

## Закреплённые зависимости

- wiringOP: `next`, commit `a7921ca2f5c124203be10d3418db70a2e15f3c10`.
- nanobind: **2.14.0**, exact release commit `86e5626728fc282637a6c338597120913dded1bb`.
- robin-map: `4ec1bf19c6a96125ea22062f38c2cf5b958e448e`.
- QEMU AArch64 acceptance bundle SHA-256: `2e7723127e679af9a32b5910e5932a952b65f664b5624839ed3fd69853acb6f8`.

## Manifest/API

- 54 public headers.
- 260 functions.
- 19 structs/classes.
- 207 struct fields.
- 26 header-visible variables.
- 664 macros total.
- 575 Python value-macros + 2 bindable function-like macros.

`audit_bindings.py`, `audit_docs.py`, backend ABI/symbol audits и manifest reproducibility gate проходят.

## Real nanobind runtime

- mock extensions: **54/54** built.
- Python package imports: **57/57**.
- mirrored pytest: **321/321 passed**.
- UART C-level PTY regression: `WIRING_SERIAL_EXT_PTY_OK`.
- production Python UART PTY regression: `PYTHON_SERIAL_PROD_PTY_OK`.
- 64-bit pseudoPins regression: `PSEUDOPINS_64BIT_OK`.

## Official stubgen

Официальный `nanobind.stubgen 2.14.0` сгенерировал **54/54** зеркальных `.pyi`.

Stub audit подтверждает:

- 260 functions;
- 19 classes/structs;
- 207 fields;
- 26 globals;
- 577 Python-exported macros.

## Production/install

- production extensions: **54/54** built.
- production smoke import: **57/57**, failures: 0.
- default CMake configuration: production backend, nanobind auto-discovery, 2 overlays auto-prepared.
- clean install-tree: **54 `.so` + 54 `.pyi` + `py.typed`**, без `__pycache__`/`.pyc`.
- installed package smoke import: **57/57**, failures: 0.

## ARM64 gate

QEMU AArch64 self-test проходит:

```text
AARCH64_QEMU_SELFTEST_OK 1122334455667788
```

Это loader/runtime self-test AArch64 ELF. Он не является тестом физического GPIO/RK3588 и не подменяет проверку на реальной Orange Pi 5.

## Итог

```text
ACCEPTANCE_OK
```

Полный вывод сохранён в `ACCEPTANCE_LOG.txt`.

## Post-acceptance upstream hardening / Orange Pi preparation

После исходного полного `ACCEPTANCE_OK` upstream overlays были реорганизованы для двух независимых PR:
PR1 с `-Werror` cleanup и PR2 только с UART API. Публичный manifest сохранился без изменений
(54 headers / 260 functions / 19 structs / 207 fields / 26 globals / 664 macros).

На финальных патчах дополнительно подтверждены 52/52 строгих AArch64 translation units без diagnostics,
реальный AArch64 LTO link/run под QEMU (`WIRINGOP_AARCH64_QEMU_OK version=2.46`), production 54/54
nanobind extensions, official stubgen 54/54, production UART PTY и install-tree 54 `.so` + 54 `.pyi` +
`py.typed`. Физический Orange Pi 5 gate в `hardware_validation/` также пройден на целевой плате: `ORANGEPI5_ACCEPTANCE_OK`.
Подробности и точные hardware/toolchain identities сохранены в `hardware_validation/LOCAL_VALIDATION_RESULTS.md`.
