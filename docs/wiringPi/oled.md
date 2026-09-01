# `wiringPi/oled.h`

Python-модуль: `wiringop.wiring_pi.oled`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `oled_close` → `oled_close(disp)`; C return `int`; адаптация `direct`.
- `oled_open` → `oled_open(disp, filename)`; C return `int`; адаптация `oled_open`.
- `oled_send` → `oled_send(disp, payload)`; C return `int`; адаптация `oled_send`.
- `oled_init` → `oled_init(disp)`; C return `int`; адаптация `direct`.
- `oled_send_buffer` → `oled_send_buffer(disp)`; C return `int`; адаптация `direct`.
- `oled_clear` → `oled_clear(disp)`; C return `void`; адаптация `direct`.
- `oled_putstr` → `oled_putstr(disp, line, str)`; C return `void`; адаптация `oled_putstr`.
- `oled_putpixel` → `oled_putpixel(disp, x, y, on)`; C return `void`; адаптация `direct`.
- `oled_putstrto` → `oled_putstrto(disp, x, y, str)`; C return `void`; адаптация `oled_putstrto`.

## Структуры

### `DisplayInfo` (`display_info`)

- `address` → `address`: `int`.
- `file` → `file`: `int`.
- `font` → `font`: `struct font_info`.
- `buffer` → `buffer`: `uint8_t[8][128]`.

### `SizedArray` (`sized_array`)

- `size` → `size`: `int`.
- `array` → `array_address`: `const uint8_t *`.

## Данные и глобальные значения

- `display_config` → `display_config` (`const unsigned char[29]`, `static`).
- `display_draw` → `display_draw` (`const unsigned char[7]`, `static`).

## Макросы

- `OLED_H` → `OLED_H`: остаётся C-only; `c_only`; определение ``.
- `OLED_I2C_ADDR` → `OLED_I2C_ADDR`: экспортируется; `value`; определение `0x3c`.
- `OLED_CTRL_BYTE_CMD_SINGLE` → `OLED_CTRL_BYTE_CMD_SINGLE`: экспортируется; `value`; определение `0x80`.
- `OLED_CTRL_BYTE_CMD_STREAM` → `OLED_CTRL_BYTE_CMD_STREAM`: экспортируется; `value`; определение `0x00`.
- `OLED_CTRL_BYTE_DATA_STREAM` → `OLED_CTRL_BYTE_DATA_STREAM`: экспортируется; `value`; определение `0x40`.
- `OLED_CMD_SET_CONTRAST` → `OLED_CMD_SET_CONTRAST`: экспортируется; `value`; определение `0x81`.
- `OLED_CMD_DISPLAY_RAM` → `OLED_CMD_DISPLAY_RAM`: экспортируется; `value`; определение `0xA4`.
- `OLED_CMD_DISPLAY_ALLON` → `OLED_CMD_DISPLAY_ALLON`: экспортируется; `value`; определение `0xA5`.
- `OLED_CMD_DISPLAY_NORMAL` → `OLED_CMD_DISPLAY_NORMAL`: экспортируется; `value`; определение `0xA6`.
- `OLED_CMD_DISPLAY_INVERTED` → `OLED_CMD_DISPLAY_INVERTED`: экспортируется; `value`; определение `0xA7`.
- `OLED_CMD_DISPLAY_OFF` → `OLED_CMD_DISPLAY_OFF`: экспортируется; `value`; определение `0xAE`.
- `OLED_CMD_DISPLAY_ON` → `OLED_CMD_DISPLAY_ON`: экспортируется; `value`; определение `0xAF`.
- `OLED_CMD_SET_MEMORY_ADDR_MODE` → `OLED_CMD_SET_MEMORY_ADDR_MODE`: экспортируется; `value`; определение `0x20`.
- `OLED_CMD_SET_COLUMN_RANGE` → `OLED_CMD_SET_COLUMN_RANGE`: экспортируется; `value`; определение `0x21`.
- `OLED_CMD_SET_PAGE_RANGE` → `OLED_CMD_SET_PAGE_RANGE`: экспортируется; `value`; определение `0x22`.
- `OLED_CMD_SET_DISPLAY_START_LINE` → `OLED_CMD_SET_DISPLAY_START_LINE`: экспортируется; `value`; определение `0x40`.
- `OLED_CMD_SET_SEGMENT_REMAP` → `OLED_CMD_SET_SEGMENT_REMAP`: экспортируется; `value`; определение `0xA1`.
- `OLED_CMD_SET_MUX_RATIO` → `OLED_CMD_SET_MUX_RATIO`: экспортируется; `value`; определение `0xA8`.
- `OLED_CMD_SET_COM_SCAN_MODE` → `OLED_CMD_SET_COM_SCAN_MODE`: экспортируется; `value`; определение `0xC8`.
- `OLED_CMD_SET_DISPLAY_OFFSET` → `OLED_CMD_SET_DISPLAY_OFFSET`: экспортируется; `value`; определение `0xD3`.
- `OLED_CMD_SET_COM_PIN_MAP` → `OLED_CMD_SET_COM_PIN_MAP`: экспортируется; `value`; определение `0xDA`.
- `OLED_CMD_NOP` → `OLED_CMD_NOP`: экспортируется; `value`; определение `0xE3`.
- `OLED_CMD_SET_DISPLAY_CLK_DIV` → `OLED_CMD_SET_DISPLAY_CLK_DIV`: экспортируется; `value`; определение `0xD5`.
- `OLED_CMD_SET_PRECHARGE` → `OLED_CMD_SET_PRECHARGE`: экспортируется; `value`; определение `0xD9`.
- `OLED_CMD_SET_VCOMH_DESELCT` → `OLED_CMD_SET_VCOMH_DESELCT`: экспортируется; `value`; определение `0xDB`.
- `OLED_CMD_SET_CHARGE_PUMP` → `OLED_CMD_SET_CHARGE_PUMP`: экспортируется; `value`; определение `0x8D`.
- `OLED_SET_PAGE_ADDRESS` → `OLED_SET_PAGE_ADDRESS`: экспортируется; `value`; определение `0xB0`.
