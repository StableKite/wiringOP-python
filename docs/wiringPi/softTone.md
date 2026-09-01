# `wiringPi/softTone.h`

Python-модуль: `wiringop.wiring_pi.soft_tone`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `softToneCreate` → `soft_tone_create(pin)`; C return `int`; адаптация `direct`.
- `softToneStop` → `soft_tone_stop(pin)`; C return `void`; адаптация `direct`.
- `softToneWrite` → `soft_tone_write(pin, freq)`; C return `void`; адаптация `direct`.

