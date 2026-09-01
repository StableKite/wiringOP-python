# `wiringPi/wiringShift.h`

Python-модуль: `wiringop.wiring_pi.wiring_shift`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `shiftIn` → `shift_in(d_pin, c_pin, order)`; C return `uint8_t`; адаптация `direct`.
- `shiftOut` → `shift_out(d_pin, c_pin, order, val)`; C return `void`; адаптация `direct`.

## Макросы

- `LSBFIRST` → `LSBFIRST`: экспортируется; `value`; определение `0`.
- `MSBFIRST` → `MSBFIRST`: экспортируется; `value`; определение `1`.
