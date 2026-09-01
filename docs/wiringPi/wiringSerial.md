# `wiringPi/wiringSerial.h`

Python-модуль: `wiringop.wiring_pi.wiring_serial`.

Модуль зеркально покрывает публичный API заголовка wiringOP. Имена Python приведены к Python-стилю; рядом сохраняются C-имена для однозначного сопоставления.

## Расширенный UART

Legacy `serialOpen()` и старый ABI сохранены без изменения. Новый API добавляет произвольный baud через Linux `termios2/BOTHER`, 5–8 бит, parity N/O/E/M/S (если поддерживает драйвер), 1/1.5/2 stop bits, XON/XOFF, RTS/CTS, modem lines, таймауты, break, exclusive/low-latency, error counters, Linux RS-485, RX FIFO trigger, wakeup, hardware/capability discovery и cancellable `serialContext`. На RK3588/DesignWare обнаруживаются FIFO, DMA description, auto RTS/CTS и расширенные RS-485 capabilities без прямого MMIO-конфликта с ядром. `SerialPort` использует один C syscall/poll path для bulk `read`/`write`, writable buffer в `read_into`, освобождает GIL на блокирующем I/O и реально реализует `cancel_read`/`cancel_write` через wakeup pipe. URL/network handlers pySerial намеренно не входят в hardware UART слой. Автоматический DSR/DTR flow-control не имеет переносимого Linux tty API и при попытке включения явно выдаёт `NotImplementedError`; ручной DTR доступен.

## Функции

- `serialOpen` → `serial_open(device, baud)`; C return `int`; адаптация `direct`.
- `serialClose` → `serial_close(fd)`; C return `void`; адаптация `direct`.
- `serialFlush` → `serial_flush(fd)`; C return `void`; адаптация `direct`.
- `serialPutchar` → `serial_putchar(fd, c)`; C return `void`; адаптация `direct`.
- `serialPuts` → `serial_puts(fd, s)`; C return `void`; адаптация `direct`.
- `serialPrintf` → `serial_printf(fd, message)`; C return `void`; адаптация `prepared_printf`.
- `serialDataAvail` → `serial_data_avail(fd)`; C return `int`; адаптация `direct`.
- `serialGetchar` → `serial_getchar(fd)`; C return `int`; адаптация `direct`.
- `serialConfigInit` → `serial_config_init(config)`; C return `void`; адаптация `serial_config_init`.
- `serialOpenConfig` → `serial_open_config(device, config)`; C return `int`; адаптация `direct`.
- `serialGetConfig` → `serial_get_config(fd, config)`; C return `int`; адаптация `serial_get_config`.
- `serialSetConfig` → `serial_set_config(fd, config)`; C return `int`; адаптация `direct`.
- `serialGetBaud` → `serial_get_baud(fd, baud)`; C return `int`; адаптация `serial_get_baud`.
- `serialSetBaud` → `serial_set_baud(fd, baud)`; C return `int`; адаптация `direct`.
- `serialRead` → `serial_read(fd, buffer, count)`; C return `ssize_t`; адаптация `serial_read`.
- `serialWrite` → `serial_write(fd, buffer, count)`; C return `ssize_t`; адаптация `serial_write`.
- `serialReadTimeout` → `serial_read_timeout(fd, buffer, count, timeout_ms, inter_byte_timeout_ms)`; C return `ssize_t`; адаптация `serial_read_timeout`.
- `serialWriteTimeout` → `serial_write_timeout(fd, buffer, count, timeout_ms)`; C return `ssize_t`; адаптация `serial_write_timeout`.
- `serialDrain` → `serial_drain(fd)`; C return `int`; адаптация `direct`.
- `serialFlushInput` → `serial_flush_input(fd)`; C return `int`; адаптация `direct`.
- `serialFlushOutput` → `serial_flush_output(fd)`; C return `int`; адаптация `direct`.
- `serialInputWaiting` → `serial_input_waiting(fd)`; C return `int`; адаптация `direct`.
- `serialOutputWaiting` → `serial_output_waiting(fd)`; C return `int`; адаптация `direct`.
- `serialSendBreak` → `serial_send_break(fd, duration_ms)`; C return `int`; адаптация `direct`.
- `serialSetBreak` → `serial_set_break(fd, enabled)`; C return `int`; адаптация `direct`.
- `serialGetModemLines` → `serial_get_modem_lines(fd, lines)`; C return `int`; адаптация `serial_get_modem_lines`.
- `serialSetModemLines` → `serial_set_modem_lines(fd, set_mask, clear_mask)`; C return `int`; адаптация `direct`.
- `serialSetRTS` → `serial_set_rts(fd, enabled)`; C return `int`; адаптация `direct`.
- `serialSetDTR` → `serial_set_dtr(fd, enabled)`; C return `int`; адаптация `direct`.
- `serialGetCTS` → `serial_get_cts(fd)`; C return `int`; адаптация `direct`.
- `serialGetDSR` → `serial_get_dsr(fd)`; C return `int`; адаптация `direct`.
- `serialGetRI` → `serial_get_ri(fd)`; C return `int`; адаптация `direct`.
- `serialGetCD` → `serial_get_cd(fd)`; C return `int`; адаптация `direct`.
- `serialSetInputFlow` → `serial_set_input_flow(fd, enabled)`; C return `int`; адаптация `direct`.
- `serialSetOutputFlow` → `serial_set_output_flow(fd, enabled)`; C return `int`; адаптация `direct`.
- `serialSetExclusive` → `serial_set_exclusive(fd, enabled)`; C return `int`; адаптация `direct`.
- `serialGetLowLatency` → `serial_get_low_latency(fd)`; C return `int`; адаптация `direct`.
- `serialSetLowLatency` → `serial_set_low_latency(fd, enabled)`; C return `int`; адаптация `direct`.
- `serialGetCounters` → `serial_get_counters(fd, counters)`; C return `int`; адаптация `serial_get_counters`.
- `serialTxEmpty` → `serial_tx_empty(fd)`; C return `int`; адаптация `direct`.
- `serialGetRS485` → `serial_get_rs485(fd, config)`; C return `int`; адаптация `serial_get_rs485`.
- `serialSetRS485` → `serial_set_rs485(fd, config)`; C return `int`; адаптация `direct`.
- `serialGetRxTrigger` → `serial_get_rx_trigger(fd)`; C return `int`; адаптация `direct`.
- `serialSetRxTrigger` → `serial_set_rx_trigger(fd, bytes)`; C return `int`; адаптация `direct`.
- `serialGetWakeup` → `serial_get_wakeup(fd)`; C return `int`; адаптация `direct`.
- `serialSetWakeup` → `serial_set_wakeup(fd, enabled)`; C return `int`; адаптация `direct`.
- `serialGetHardwareInfo` → `serial_get_hardware_info(fd, info)`; C return `int`; адаптация `serial_get_hardware_info`.
- `serialGetCapabilities` → `serial_get_capabilities(fd, capabilities)`; C return `int`; адаптация `serial_get_capabilities`.
- `serialContextOpen` → `serial_context_open(device, config)`; C return `serialContext *`; адаптация `serial_context_open`.
- `serialContextFromFd` → `serial_context_from_fd(fd, take_ownership)`; C return `serialContext *`; адаптация `serial_context_from_fd`.
- `serialContextClose` → `serial_context_close(context)`; C return `void`; адаптация `serial_context_close`.
- `serialContextGetFd` → `serial_context_get_fd(context)`; C return `int`; адаптация `serial_context_get_fd`.
- `serialContextRead` → `serial_context_read(context, buffer, count, timeout_ms, inter_byte_timeout_ms)`; C return `ssize_t`; адаптация `serial_context_read`.
- `serialContextWrite` → `serial_context_write(context, buffer, count, timeout_ms)`; C return `ssize_t`; адаптация `serial_context_write`.
- `serialContextCancelRead` → `serial_context_cancel_read(context)`; C return `int`; адаптация `serial_context_cancel_read`.
- `serialContextCancelWrite` → `serial_context_cancel_write(context)`; C return `int`; адаптация `serial_context_cancel_write`.

## Структуры

### `SerialConfig` (`serialConfig`)

- `structSize` → `struct_size`: `uint32_t`.
- `version` → `version`: `uint32_t`.
- `baud` → `baud`: `uint32_t`.
- `dataBits` → `data_bits`: `uint8_t`.
- `parity` → `parity`: `uint8_t`.
- `stopBits` → `stop_bits`: `uint8_t`.
- `flowControl` → `flow_control`: `uint8_t`.
- `xonChar` → `xon_char`: `uint8_t`.
- `xoffChar` → `xoff_char`: `uint8_t`.
- `vmin` → `vmin`: `uint8_t`.
- `vtime` → `vtime`: `uint8_t`.
- `reserved` → `reserved`: `uint32_t[4]`.

### `SerialRS485Config` (`serialRS485Config`)

- `structSize` → `struct_size`: `uint32_t`.
- `flags` → `flags`: `uint32_t`.
- `delayBeforeSendMs` → `delay_before_send_ms`: `uint32_t`.
- `delayAfterSendMs` → `delay_after_send_ms`: `uint32_t`.
- `receiveAddress` → `receive_address`: `uint8_t`.
- `destinationAddress` → `destination_address`: `uint8_t`.
- `reserved8` → `reserved8`: `uint8_t[2]`.
- `reserved` → `reserved`: `uint32_t[4]`.

### `SerialCounters` (`serialCounters`)

- `structSize` → `struct_size`: `uint32_t`.
- `cts` → `cts`: `uint32_t`.
- `dsr` → `dsr`: `uint32_t`.
- `rng` → `rng`: `uint32_t`.
- `dcd` → `dcd`: `uint32_t`.
- `rx` → `rx`: `uint32_t`.
- `tx` → `tx`: `uint32_t`.
- `frame` → `frame`: `uint32_t`.
- `overrun` → `overrun`: `uint32_t`.
- `parity` → `parity`: `uint32_t`.
- `brk` → `brk`: `uint32_t`.
- `bufOverrun` → `buf_overrun`: `uint32_t`.
- `reserved` → `reserved`: `uint32_t[4]`.

### `SerialHardwareInfo` (`serialHardwareInfo`)

- `structSize` → `struct_size`: `uint32_t`.
- `hardwareType` → `hardware_type`: `uint32_t`.
- `fifoSize` → `fifo_size`: `uint32_t`.
- `baudBase` → `baud_base`: `uint32_t`.
- `portType` → `port_type`: `uint32_t`.
- `line` → `line`: `uint32_t`.
- `capabilities` → `capabilities`: `uint64_t`.
- `reserved` → `reserved`: `uint32_t[6]`.

## Макросы

- `__WIRING_SERIAL_H__` → `WIRING_SERIAL_H`: остаётся C-only; `c_only`; определение ``.
- `SERIAL_CONFIG_VERSION` → `SERIAL_CONFIG_VERSION`: экспортируется; `value`; определение `1U`.
- `SERIAL_CONFIG_STRUCT_SIZE` → `SERIAL_CONFIG_STRUCT_SIZE`: экспортируется; `value`; определение `((uint32_t) sizeof (serialConfig))`.
- `SERIAL_PARITY_NONE` → `SERIAL_PARITY_NONE`: экспортируется; `value`; определение `0U`.
- `SERIAL_PARITY_ODD` → `SERIAL_PARITY_ODD`: экспортируется; `value`; определение `1U`.
- `SERIAL_PARITY_EVEN` → `SERIAL_PARITY_EVEN`: экспортируется; `value`; определение `2U`.
- `SERIAL_PARITY_MARK` → `SERIAL_PARITY_MARK`: экспортируется; `value`; определение `3U`.
- `SERIAL_PARITY_SPACE` → `SERIAL_PARITY_SPACE`: экспортируется; `value`; определение `4U`.
- `SERIAL_STOP_BITS_ONE` → `SERIAL_STOP_BITS_ONE`: экспортируется; `value`; определение `1U`.
- `SERIAL_STOP_BITS_ONE_POINT_FIVE` → `SERIAL_STOP_BITS_ONE_POINT_FIVE`: экспортируется; `value`; определение `2U`.
- `SERIAL_STOP_BITS_TWO` → `SERIAL_STOP_BITS_TWO`: экспортируется; `value`; определение `3U`.
- `SERIAL_FLOW_NONE` → `SERIAL_FLOW_NONE`: экспортируется; `value`; определение `0U`.
- `SERIAL_FLOW_XON_XOFF` → `SERIAL_FLOW_XON_XOFF`: экспортируется; `value`; определение `(1U << 0)`.
- `SERIAL_FLOW_RTS_CTS` → `SERIAL_FLOW_RTS_CTS`: экспортируется; `value`; определение `(1U << 1)`.
- `SERIAL_MODEM_RTS` → `SERIAL_MODEM_RTS`: экспортируется; `value`; определение `(1U << 0)`.
- `SERIAL_MODEM_DTR` → `SERIAL_MODEM_DTR`: экспортируется; `value`; определение `(1U << 1)`.
- `SERIAL_MODEM_CTS` → `SERIAL_MODEM_CTS`: экспортируется; `value`; определение `(1U << 2)`.
- `SERIAL_MODEM_DSR` → `SERIAL_MODEM_DSR`: экспортируется; `value`; определение `(1U << 3)`.
- `SERIAL_MODEM_RI` → `SERIAL_MODEM_RI`: экспортируется; `value`; определение `(1U << 4)`.
- `SERIAL_MODEM_CD` → `SERIAL_MODEM_CD`: экспортируется; `value`; определение `(1U << 5)`.
- `SERIAL_MODEM_LOOP` → `SERIAL_MODEM_LOOP`: экспортируется; `value`; определение `(1U << 6)`.
- `SERIAL_RS485_ENABLED` → `SERIAL_RS485_ENABLED`: экспортируется; `value`; определение `(1U << 0)`.
- `SERIAL_RS485_RTS_ON_SEND` → `SERIAL_RS485_RTS_ON_SEND`: экспортируется; `value`; определение `(1U << 1)`.
- `SERIAL_RS485_RTS_AFTER_SEND` → `SERIAL_RS485_RTS_AFTER_SEND`: экспортируется; `value`; определение `(1U << 2)`.
- `SERIAL_RS485_RX_DURING_TX` → `SERIAL_RS485_RX_DURING_TX`: экспортируется; `value`; определение `(1U << 3)`.
- `SERIAL_RS485_TERMINATE_BUS` → `SERIAL_RS485_TERMINATE_BUS`: экспортируется; `value`; определение `(1U << 4)`.
- `SERIAL_RS485_ADDRESS_MODE` → `SERIAL_RS485_ADDRESS_MODE`: экспортируется; `value`; определение `(1U << 5)`.
- `SERIAL_RS485_RX_ADDRESS` → `SERIAL_RS485_RX_ADDRESS`: экспортируется; `value`; определение `(1U << 6)`.
- `SERIAL_RS485_DEST_ADDRESS` → `SERIAL_RS485_DEST_ADDRESS`: экспортируется; `value`; определение `(1U << 7)`.
- `SERIAL_RS485_MODE_RS422` → `SERIAL_RS485_MODE_RS422`: экспортируется; `value`; определение `(1U << 8)`.
- `SERIAL_CAP_CUSTOM_BAUD` → `SERIAL_CAP_CUSTOM_BAUD`: экспортируется; `value`; определение `(1ULL << 0)`.
- `SERIAL_CAP_MARK_SPACE_PARITY` → `SERIAL_CAP_MARK_SPACE_PARITY`: экспортируется; `value`; определение `(1ULL << 1)`.
- `SERIAL_CAP_XON_XOFF` → `SERIAL_CAP_XON_XOFF`: экспортируется; `value`; определение `(1ULL << 2)`.
- `SERIAL_CAP_RTS_CTS` → `SERIAL_CAP_RTS_CTS`: экспортируется; `value`; определение `(1ULL << 3)`.
- `SERIAL_CAP_MODEM_CONTROL` → `SERIAL_CAP_MODEM_CONTROL`: экспортируется; `value`; определение `(1ULL << 4)`.
- `SERIAL_CAP_MODEM_STATUS` → `SERIAL_CAP_MODEM_STATUS`: экспортируется; `value`; определение `(1ULL << 5)`.
- `SERIAL_CAP_EXCLUSIVE` → `SERIAL_CAP_EXCLUSIVE`: экспортируется; `value`; определение `(1ULL << 6)`.
- `SERIAL_CAP_LOW_LATENCY` → `SERIAL_CAP_LOW_LATENCY`: экспортируется; `value`; определение `(1ULL << 7)`.
- `SERIAL_CAP_RS485` → `SERIAL_CAP_RS485`: экспортируется; `value`; определение `(1ULL << 8)`.
- `SERIAL_CAP_ICOUNT` → `SERIAL_CAP_ICOUNT`: экспортируется; `value`; определение `(1ULL << 9)`.
- `SERIAL_CAP_TX_EMPTY` → `SERIAL_CAP_TX_EMPTY`: экспортируется; `value`; определение `(1ULL << 10)`.
- `SERIAL_CAP_RX_TRIGGER` → `SERIAL_CAP_RX_TRIGGER`: экспортируется; `value`; определение `(1ULL << 11)`.
- `SERIAL_CAP_WAKEUP` → `SERIAL_CAP_WAKEUP`: экспортируется; `value`; определение `(1ULL << 12)`.
- `SERIAL_CAP_8250` → `SERIAL_CAP_8250`: экспортируется; `value`; определение `(1ULL << 13)`.
- `SERIAL_CAP_DW_APB_UART` → `SERIAL_CAP_DW_APB_UART`: экспортируется; `value`; определение `(1ULL << 14)`.
- `SERIAL_CAP_RK3588_UART` → `SERIAL_CAP_RK3588_UART`: экспортируется; `value`; определение `(1ULL << 15)`.
- `SERIAL_CAP_DMA_DESCRIBED` → `SERIAL_CAP_DMA_DESCRIBED`: экспортируется; `value`; определение `(1ULL << 16)`.
- `SERIAL_CAP_AUTO_RTS_CTS` → `SERIAL_CAP_AUTO_RTS_CTS`: экспортируется; `value`; определение `(1ULL << 17)`.
- `SERIAL_CAP_FIFO` → `SERIAL_CAP_FIFO`: экспортируется; `value`; определение `(1ULL << 18)`.
- `SERIAL_CAP_CANCEL_IO` → `SERIAL_CAP_CANCEL_IO`: экспортируется; `value`; определение `(1ULL << 19)`.
- `SERIAL_HARDWARE_UNKNOWN` → `SERIAL_HARDWARE_UNKNOWN`: экспортируется; `value`; определение `0U`.
- `SERIAL_HARDWARE_8250` → `SERIAL_HARDWARE_8250`: экспортируется; `value`; определение `1U`.
- `SERIAL_HARDWARE_DW_APB_UART` → `SERIAL_HARDWARE_DW_APB_UART`: экспортируется; `value`; определение `2U`.
- `SERIAL_HARDWARE_RK3588_UART` → `SERIAL_HARDWARE_RK3588_UART`: экспортируется; `value`; определение `3U`.
