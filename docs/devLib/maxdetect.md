# `devLib/maxdetect.h`

Python-модуль: `wiringop.dev_lib.maxdetect`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `maxDetectRead` → `max_detect_read(pin, buffer)`; C return `int`; адаптация `maxdetect_read`.
- `readRHT03` → `read_rht03(pin, temp, rh)`; C return `int`; адаптация `rht03_read`.

