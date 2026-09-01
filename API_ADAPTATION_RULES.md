# Правила Pythonic adapters

## Общий принцип

Публичный Python API не должен заставлять пользователя вручную работать с C pointers, output buffers, variadic formatting или unsafe ownership, если это можно естественно представить Python типом.

## Functions

Обычные scalar/string функции связывать напрямую через nanobind с `nb::arg()`.

## Output pointers

C API вида:

```c
int f(int *a, int *b);
```

в Python должен возвращать нормальное значение/tuple, например:

```python
status, a, b = f(...)
```

или только meaningful values, если status может быть выражен exception/normal semantics. Решение фиксировать в docs и stubs.

## Buffers

### SPI

`wiringPiSPIDataRW` должен принимать writable contiguous Python buffer (`bytearray`, writable memoryview) и изменять его **на месте**.

Read-only `bytes` для API, которое пишет в буфер, должно отклоняться понятным исключением.

### W25Q64

Read operations должны возвращать `bytes`.

Write operations должны принимать Python buffer/bytes-like input.

Page limits/size constraints нужно валидировать и тестировать.

## Strings / variadic

C variadic printf-like APIs нельзя биндинговать как произвольный C varargs. Сделать безопасную Python wrapper семантику, обычно принимающую уже готовую строку.

## Callbacks

`wiringPiISR` и `piThreadCreate` должны принимать Python callable.

Требования:

- trampoline хранит Python callable с корректным lifetime;
- callback входит в GIL (`PyGILState_Ensure` или корректный nanobind эквивалент);
- Python exception не должен silently corrupt процесс — использовать unraisable/error reporting;
- thread callback освобождать после завершения, если lifetime одноразовый;
- ISR slots покрывают весь upstream `MAX_PIN_NUM`, а не hardcoded 64, если upstream значение изменится.

В конкретном зафиксированном commit ранее наблюдалось `MAX_PIN_NUM = 0x40`.

## Raw pointer fields

Низкоуровневые struct fields типа raw pointer/function pointer не выдавать за безопасные Python-owned objects.

Предыдущая выбранная политика:

```text
foo* ptr → ptr_address: int
function pointer → callback_address: int
```

Для массивов/буферов использовать безопасные Python representations, где возможно.

## Globals

Header-visible extern globals и meaningful static data экспортировать через явные accessors/properties, а не unsafe прямое присваивание, если C ABI/lifetime этого не гарантирует.

## Macros

Object-like macro экспортировать как Python constant только если компилятор подтверждает, что macro является самостоятельным C/C++ expression в контексте соответствующего header.

Контекстные/служебные macros документировать как C-only, но не притворяться Python value.

Function-like macros:

- `RK3588_GPIO_BIT(x)` → Python function;
- `RK3399_GPIO_BIT(x)` → Python function;
- `PI_THREAD(X)` — declaration helper, C-only, не runtime Python API.

## Upstream missing symbols

В текущем wiringOP header объявляет, но linker symbols отсутствуют:

```text
digitalRead8
digitalWrite8
wiringPiSetupPiFace
wiringPiSetupPiFaceForGpioProg
```

Python API должен сохранять соответствующие Python names, но при вызове давать **явный `NotImplementedError`** с объяснением, а не создавать broken linker reference.

### getResponce typo

Header содержит опечатку `getResponce`, а реальная реализация — `getResponse`.

Выбранная совместимость:

```text
getResponse → get_response
getResponce → get_response_legacy
```

`get_response_legacy` вызывает существующий `getResponse`, но docs должны явно сказать, что это upstream typo compatibility alias.
