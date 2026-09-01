# `wiringPi/wiringPiI2C.h`

Python-модуль: `wiringop.wiring_pi.wiring_pi_i2c`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `wiringPiI2CRead` → `wiring_pi_i2c_read(fd)`; C return `int`; адаптация `direct`.
- `wiringPiI2CReadReg8` → `wiring_pi_i2c_read_reg8(fd, reg)`; C return `int`; адаптация `direct`.
- `wiringPiI2CReadReg16` → `wiring_pi_i2c_read_reg16(fd, reg)`; C return `int`; адаптация `direct`.
- `wiringPiI2CWrite` → `wiring_pi_i2c_write(fd, data)`; C return `int`; адаптация `direct`.
- `wiringPiI2CWriteReg8` → `wiring_pi_i2c_write_reg8(fd, reg, data)`; C return `int`; адаптация `direct`.
- `wiringPiI2CWriteReg16` → `wiring_pi_i2c_write_reg16(fd, reg, data)`; C return `int`; адаптация `direct`.
- `wiringPiI2CSetupInterface` → `wiring_pi_i2c_setup_interface(device, dev_id)`; C return `int`; адаптация `direct`.
- `wiringPiI2CSetup` → `wiring_pi_i2c_setup(dev_id)`; C return `int`; адаптация `direct`.

