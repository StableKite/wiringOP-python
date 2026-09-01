# `devLib/piNes.h`

Python-модуль: `wiringop.dev_lib.pi_nes`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `setupNesJoystick` → `setup_nes_joystick(d_pin, c_pin, l_pin)`; C return `int`; адаптация `direct`.
- `readNesJoystick` → `read_nes_joystick(joystick)`; C return `unsigned int`; адаптация `direct`.

## Макросы

- `MAX_NES_JOYSTICKS` → `MAX_NES_JOYSTICKS`: экспортируется; `value`; определение `8`.
- `NES_RIGHT` → `NES_RIGHT`: экспортируется; `value`; определение `0x01`.
- `NES_LEFT` → `NES_LEFT`: экспортируется; `value`; определение `0x02`.
- `NES_DOWN` → `NES_DOWN`: экспортируется; `value`; определение `0x04`.
- `NES_UP` → `NES_UP`: экспортируется; `value`; определение `0x08`.
- `NES_START` → `NES_START`: экспортируется; `value`; определение `0x10`.
- `NES_SELECT` → `NES_SELECT`: экспортируется; `value`; определение `0x20`.
- `NES_B` → `NES_B`: экспортируется; `value`; определение `0x40`.
- `NES_A` → `NES_A`: экспортируется; `value`; определение `0x80`.
