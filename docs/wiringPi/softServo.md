# `wiringPi/softServo.h`

Python-модуль: `wiringop.wiring_pi.soft_servo`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `softServoWrite` → `soft_servo_write(pin, value)`; C return `void`; адаптация `direct`.
- `softServoSetup` → `soft_servo_setup(p0, p1, p2, p3, p4, p5, p6, p7)`; C return `int`; адаптация `direct`.

