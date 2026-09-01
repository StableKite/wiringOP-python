# `wiringPi/wiringPiSPI.h`

Python-модуль: `wiringop.wiring_pi.wiring_pi_spi`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `wiringPiSPIGetFd` → `wiring_pi_spi_get_fd(channel)`; C return `int`; адаптация `direct`.
- `wiringPiSPIDataRW` → `wiring_pi_spi_data_rw(channel, data, len)`; C return `int`; адаптация `spi_inout_buffer`.
- `wiringPiSPISetupMode` → `wiring_pi_spi_setup_mode(channel, port, speed, mode)`; C return `int`; адаптация `direct`.
- `wiringPiSPISetup` → `wiring_pi_spi_setup(channel, speed)`; C return `int`; адаптация `direct`.

