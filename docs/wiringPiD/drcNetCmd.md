# `wiringPiD/drcNetCmd.h`

Python-модуль: `wiringop.wiring_pi_d.drc_net_cmd`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Структуры

### `DrcNetComStruct` (`drcNetComStruct`)

- `pin` → `pin`: `uint32_t`.
- `cmd` → `cmd`: `uint32_t`.
- `data` → `data`: `uint32_t`.

## Макросы

- `DEFAULT_SERVER_PORT` → `DEFAULT_SERVER_PORT`: экспортируется; `value`; определение `6124`.
- `DRCN_PIN_MODE` → `DRCN_PIN_MODE`: экспортируется; `value`; определение `1`.
- `DRCN_PULL_UP_DN` → `DRCN_PULL_UP_DN`: экспортируется; `value`; определение `2`.
- `DRCN_DIGITAL_WRITE` → `DRCN_DIGITAL_WRITE`: экспортируется; `value`; определение `3`.
- `DRCN_DIGITAL_WRITE8` → `DRCN_DIGITAL_WRITE8`: экспортируется; `value`; определение `4`.
- `DRCN_ANALOG_WRITE` → `DRCN_ANALOG_WRITE`: экспортируется; `value`; определение `5`.
- `DRCN_PWM_WRITE` → `DRCN_PWM_WRITE`: экспортируется; `value`; определение `6`.
- `DRCN_DIGITAL_READ` → `DRCN_DIGITAL_READ`: экспортируется; `value`; определение `7`.
- `DRCN_DIGITAL_READ8` → `DRCN_DIGITAL_READ8`: экспортируется; `value`; определение `8`.
- `DRCN_ANALOG_READ` → `DRCN_ANALOG_READ`: экспортируется; `value`; определение `9`.
