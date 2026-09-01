# `devLib/piGlow.h`

Python-модуль: `wiringop.dev_lib.pi_glow`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `piGlow1` → `pi_glow1(leg, ring, intensity)`; C return `void`; адаптация `direct`.
- `piGlowLeg` → `pi_glow_leg(leg, intensity)`; C return `void`; адаптация `direct`.
- `piGlowRing` → `pi_glow_ring(ring, intensity)`; C return `void`; адаптация `direct`.
- `piGlowSetup` → `pi_glow_setup(clear)`; C return `void`; адаптация `direct`.

## Макросы

- `PIGLOW_RED` → `PIGLOW_RED`: экспортируется; `value`; определение `0`.
- `PIGLOW_ORANGE` → `PIGLOW_ORANGE`: экспортируется; `value`; определение `1`.
- `PIGLOW_YELLOW` → `PIGLOW_YELLOW`: экспортируется; `value`; определение `2`.
- `PIGLOW_GREEN` → `PIGLOW_GREEN`: экспортируется; `value`; определение `3`.
- `PIGLOW_BLUE` → `PIGLOW_BLUE`: экспортируется; `value`; определение `4`.
- `PIGLOW_WHITE` → `PIGLOW_WHITE`: экспортируется; `value`; определение `5`.
