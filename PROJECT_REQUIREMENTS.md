# Требования пользователя — обязательный контракт проекта

Это требования, которые нельзя ослаблять без явного нового указания пользователя.

## Основная цель

Реализовать **полные nanobind bindings для wiringOP** с Pythonic API и полным тестовым/документационным/stubgen покрытием.

## Структура репозитория

В корне проекта обязательно:

```text
extern/
  wiringOP/                 git submodule
src/                        nanobind C++ модули
tests/                      зеркальные Python tests
docs/                       зеркальная документация на русском
stubs/                      сгенерированные .pyi
tools/                      генераторы/audits/acceptance
support/mock_backend/       hardware-free C ABI backend
pyproject.toml
CMakeLists.txt
README.md
LICENSE
```

### wiringOP

`wiringOP` должен находиться в `extern/wiringOP` именно как **git submodule/gitlink**, а не как случайно скопированная директория.

Зафиксированный upstream commit:

```text
a7921ca2f5c124203be10d3418db70a2e15f3c10
```

## Зеркальность

Для каждого из 54 upstream header-файлов должен существовать соответствующий публичный binder `.cpp` с тем же относительным путём и basename.

Пример:

```text
extern/wiringOP/wiringPi/wiringPiSPI.h
src/wiringPi/wiringPiSPI.cpp
tests/wiringPi/wiringPiSPI.py
docs/wiringPi/wiringPiSPI.md
stubs/wiringPi/wiringPiSPI.pyi
```

### Имена тестов

**Никакого `test_` префикса.**

Имя файла в `tests` должно совпадать с `.cpp`:

```text
src/devLib/piFace.cpp
→ tests/devLib/piFace.py
```

Pytest нужно настроить через `pyproject.toml`, например:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["*.py"]
```

### Stubs

Сгенерированные `.pyi` должны **зеркалить все публичные C++ module files**.

```text
src/<path>/<name>.cpp
→ stubs/<path>/<name>.pyi
```

Если есть технический `src/wiringop.cpp`, который является публичным entrypoint module, ему также должны соответствовать test/doc/stub. Внутренние support `.cpp` (например callback trampoline implementation), которые не создают Python submodule, должны быть явно исключены из публичного mirror contract и проверяться отдельным audit'ом.

## Полнота API

Нужно полное покрытие всех публичных headers, включая:

- функции;
- структуры и **каждое поле**;
- anonymous/typedef structs;
- enums, если присутствуют;
- extern/global/static header-visible data, если они являются частью публичного API;
- object-like macros;
- bindable function-like macros;
- conditional macros — с корректным учётом препроцессорных условий.

Нельзя считать «покрытием» только наличие C++ файла на header.

## Python naming style

Публичный Python API должен соответствовать принятому Python стилю:

- функции/методы/модули: `snake_case`;
- классы: `CapWords`;
- константы: `UPPER_SNAKE_CASE`;
- параметрам нужно дать нормальные имена через `nb::arg(...)`, чтобы stubgen не создавал `arg0`, `arg1`.

Нужно корректно обрабатывать акронимы:

```text
I2C → i2c
SPI → spi
GPIO → gpio
PWM → pwm
OLED → oled
W25Q64 → w25q64
WPi/WPI → wpi
```

Не допускать уродливых имён вроде `i2_c`, `w25_q64`, `load_w_pi_extension`.

## Документация

`docs/**/*.md` должна быть:

- зеркальной;
- полностью на русском языке;
- полной;
- человекочитаемой;
- без воды;
- описывать именно Python API, а не просто копировать C prototypes;
- отдельно объяснять адаптации buffers, tuples, callbacks, ownership/raw pointers и ограничения hardware/upstream.

## Тесты

Нужно **полное runtime покрытие bindings тестами**, а не только `hasattr`.

Hardware-free tests должны запускаться на mock backend с тем же C ABI, что wiringOP.

Каждый mapped public function должен быть реально вызван хотя бы один раз, где это безопасно и осмысленно.

Отдельно тестировать:

- buffers;
- output pointer → tuple/value adapters;
- strings/bytes;
- callbacks/GIL;
- structures/fields;
- globals/accessors;
- constants;
- ошибки для upstream-missing functions;
- stub signatures.

## nanobind.stubgen

Требуется **полное покрытие настоящим `nanobind.stubgen`**.

Не вручную написанные stubs как финальный результат.

Acceptance должен:

1. собрать extension настоящим nanobind;
2. импортировать модули;
3. запустить `nanobind.stubgen`;
4. получить зеркальные `.pyi`;
5. проверить каждую функцию, класс, поле, global accessor и экспортируемую константу по manifest.
