# Архитектура реализации

## 1. Manifest как источник правды

Рекомендуемый pipeline:

```text
extern/wiringOP headers
→ Clang AST JSON
→ preprocessor macro scan
→ api_manifest.json
→ binders/tests/docs/mock generation
→ independent audits
```

Manifest должен хранить минимум:

- header path;
- C symbol name;
- exact return type;
- parameters с именами и C types;
- variadic flag;
- struct/typedef record metadata;
- fields;
- enums;
- globals/static objects;
- macros и классификацию;
- Python module path;
- Python symbol name;
- adaptation kind;
- known-upstream-gap status.

### Clang AST

Простой regex parser недостаточен. Ранее он терял:

- pointer return types (`wiringPiNewNode`, `wiringPiFindNode`, `getClientIP`);
- `wiringPiISR`/`piThreadCreate`;
- anonymous typedef structs.

Для anonymous structs нужно связывать `TypedefDecl` с его `ownedTagDecl`/`RecordDecl` ID и собирать поля.

## 2. Header mirror

Подтверждено 54 headers.

Для каждого:

```text
src/<relative-header-without-.h>.cpp
tests/<same>.py
docs/<same>.md
stubs/<same>.pyi
```

Корневой entrypoint `src/wiringop.cpp` допустим дополнительно как публичный модуль; если он есть, его также зеркалить tests/docs/stubs.

## 3. Python package/module layout

Предыдущая выбранная схема:

```text
wiringop.wiring_pi.wiring_pi
wiringop.wiring_pi.wiring_pi_spi
wiringop.wiring_pi.wiring_pi_i2c
wiringop.wiring_pi.serial
wiringop.dev_lib.lcd
...
```

Физическое дерево C++/tests/docs/stubs при этом остаётся с upstream basename (например `wiringPiSPI.cpp`), а Python import path — Pythonic.

## 4. Mock backend

Нужен отдельный:

```text
support/mock_backend/<same relative header path>.c
```

или эквивалентный зеркальный C ABI набор.

Требования:

- те же C symbols/signatures;
- никакого `/dev/mem`, GPIO/I2C/SPI real hardware;
- детерминированные результаты;
- writable buffers модифицировать предсказуемо;
- callbacks вызывать детерминированно;
- output pointers заполнять значениями;
- globals иметь стабильные значения.

Mock symbol audit должен компилировать и relocatable-link весь backend, чтобы ловить duplicates/missing symbols.

## 5. Production backend

wiringOP сам не модифицировать.

CMake должен собирать требуемые upstream `.c` как внутренние static/object targets и линковать nanobind extension поверх них.

Особое внимание: `softServo.c` ранее был обнаружен как файл, который может не попадать в upstream Makefile так, как ожидается. Список source files должен быть явным/аудируемым и сравниваться с manifest/linker symbols.

## 6. Independent audits

Минимум:

### Layout audit

Проверяет:

```text
54 upstream headers
↔ 54 header binders
↔ 54 tests
↔ 54 docs
↔ 54 header stub targets
```

Плюс отдельно public root module, если он есть.

Падает при любом `test_*.py`.

### Source↔manifest audit

Проверяет каждую функцию/структуру/поле/global/macro против фактического binder source.

### Production symbol audit

Компилирует production C backend и через `nm` сравнивает public declared functions с определёнными global symbols.

### Mock symbol audit

То же для mock C ABI.

### Documentation audit

Требует, чтобы каждый C symbol + Python name присутствовал в зеркальном `.md`.

### Stub audit

После настоящего stubgen проверяет все Python symbols по manifest.
