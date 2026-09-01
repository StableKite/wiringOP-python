# `devLib/lcd.h`

Python-модуль: `wiringop.dev_lib.lcd`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `lcdHome` → `lcd_home(fd)`; C return `void`; адаптация `direct`.
- `lcdClear` → `lcd_clear(fd)`; C return `void`; адаптация `direct`.
- `lcdDisplay` → `lcd_display(fd, state)`; C return `void`; адаптация `direct`.
- `lcdCursor` → `lcd_cursor(fd, state)`; C return `void`; адаптация `direct`.
- `lcdCursorBlink` → `lcd_cursor_blink(fd, state)`; C return `void`; адаптация `direct`.
- `lcdSendCommand` → `lcd_send_command(fd, command)`; C return `void`; адаптация `direct`.
- `lcdPosition` → `lcd_position(fd, x, y)`; C return `void`; адаптация `direct`.
- `lcdCharDef` → `lcd_char_def(fd, index, data)`; C return `void`; адаптация `lcd_char_def`.
- `lcdPutchar` → `lcd_putchar(fd, data)`; C return `void`; адаптация `direct`.
- `lcdPuts` → `lcd_puts(fd, string)`; C return `void`; адаптация `direct`.
- `lcdPrintf` → `lcd_printf(fd, message)`; C return `void`; адаптация `prepared_printf`.
- `lcdInit` → `lcd_init(rows, cols, bits, rs, strb, d0, d1, d2, d3, d4, d5, d6, d7)`; C return `int`; адаптация `direct`.

## Макросы

- `MAX_LCDS` → `MAX_LCDS`: экспортируется; `value`; определение `8`.
