# `devLib/scrollPhat.h`

Python-модуль: `wiringop.dev_lib.scroll_phat`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Функции

- `scrollPhatPoint` → `scroll_phat_point(x, y, colour)`; C return `void`; адаптация `direct`.
- `scrollPhatLine` → `scroll_phat_line(x0, y0, x1, y1, colour)`; C return `void`; адаптация `direct`.
- `scrollPhatLineTo` → `scroll_phat_line_to(x, y, colour)`; C return `void`; адаптация `direct`.
- `scrollPhatRectangle` → `scroll_phat_rectangle(x1, y1, x2, y2, colour, filled)`; C return `void`; адаптация `direct`.
- `scrollPhatUpdate` → `scroll_phat_update()`; C return `void`; адаптация `direct`.
- `scrollPhatClear` → `scroll_phat_clear()`; C return `void`; адаптация `direct`.
- `scrollPhatPutchar` → `scroll_phat_putchar(c)`; C return `int`; адаптация `direct`.
- `scrollPhatPuts` → `scroll_phat_puts(str)`; C return `void`; адаптация `direct`.
- `scrollPhatPrintf` → `scroll_phat_printf(message)`; C return `void`; адаптация `prepared_printf`.
- `scrollPhatPrintSpeed` → `scroll_phat_print_speed(cps10)`; C return `void`; адаптация `direct`.
- `scrollPhatIntensity` → `scroll_phat_intensity(percent)`; C return `void`; адаптация `direct`.
- `scrollPhatSetup` → `scroll_phat_setup()`; C return `int`; адаптация `direct`.

