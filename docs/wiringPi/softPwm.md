# `wiringPi/softPwm.h`

Python-модуль: `wiringop.wiring_pi.soft_pwm`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `softPwmCreate` → `soft_pwm_create(pin, value, range)`; C return `int`; адаптация `direct`.
- `softPwmWrite` → `soft_pwm_write(pin, value)`; C return `void`; адаптация `direct`.
- `softPwmStop` → `soft_pwm_stop(pin)`; C return `void`; адаптация `direct`.

