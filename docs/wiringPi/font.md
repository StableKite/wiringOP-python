# `wiringPi/font.h`

Python-модуль: `wiringop.wiring_pi.font`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Структуры

### `FontInfo` (`font_info`)

- `width` → `width`: `uint8_t`.
- `height` → `height`: `uint8_t`.
- `spacing` → `spacing`: `uint8_t`.
- `offset` → `offset`: `uint8_t`.
- `data` → `data_address`: `uint8_t *`.

## Данные и глобальные значения

- `font1_data` → `font1_data` (`const uint8_t[1280]`, `static`).
- `font2_data` → `font2_data` (`const uint8_t[95][6]`, `static`).
- `font3_data` → `font3_data` (`const uint8_t[1425][5]`, `static`).
- `font1` → `font1` (`struct font_info`, `static`).
- `font2` → `font2` (`struct font_info`, `static`).
- `font3` → `font3` (`struct font_info`, `static`).

## Макросы

- `FONT_H` → `FONT_H`: остаётся C-only; `c_only`; определение ``.
