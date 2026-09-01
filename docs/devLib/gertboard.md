# `devLib/gertboard.h`

Python-модуль: `wiringop.dev_lib.gertboard`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `gertboardAnalogWrite` → `gertboard_analog_write(chan, value)`; C return `void`; адаптация `direct`.
- `gertboardAnalogRead` → `gertboard_analog_read(chan)`; C return `int`; адаптация `direct`.
- `gertboardSPISetup` → `gertboard_spi_setup()`; C return `int`; адаптация `direct`.
- `gertboardAnalogSetup` → `gertboard_analog_setup(pin_base)`; C return `int`; адаптация `direct`.

