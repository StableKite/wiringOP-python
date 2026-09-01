"""nanobind bindings for wiringPi/oled.h"""

import wiringop.wiring_pi.font


class DisplayInfo:
    def __init__(self) -> None: ...

    @property
    def address(self) -> int: ...

    @address.setter
    def address(self, arg: int, /) -> None: ...

    @property
    def file(self) -> int: ...

    @file.setter
    def file(self, arg: int, /) -> None: ...

    @property
    def font(self) -> wiringop.wiring_pi.font.FontInfo: ...

    @font.setter
    def font(self, arg: wiringop.wiring_pi.font.FontInfo, /) -> None: ...

    @property
    def buffer(self) -> bytes: ...

    @buffer.setter
    def buffer(self, arg: bytes, /) -> None: ...

class SizedArray:
    def __init__(self) -> None: ...

    @property
    def size(self) -> int: ...

    @size.setter
    def size(self, arg: int, /) -> None: ...

    @property
    def array_address(self) -> int: ...

    @array_address.setter
    def array_address(self, arg: int, /) -> None: ...

def oled_close(disp: DisplayInfo) -> int: ...

def oled_open(disp: DisplayInfo, filename: str) -> int: ...

def oled_send(disp: DisplayInfo, payload: object) -> int: ...

def oled_init(disp: DisplayInfo) -> int: ...

def oled_send_buffer(disp: DisplayInfo) -> int: ...

def oled_clear(disp: DisplayInfo) -> None: ...

def oled_putstr(disp: DisplayInfo, line: int, text: str) -> None: ...

def oled_putpixel(disp: DisplayInfo, x: int, y: int, on: int) -> None: ...

def oled_putstrto(disp: DisplayInfo, x: int, y: int, text: str) -> None: ...

display_config: bytes = ...

display_draw: bytes = ...

OLED_I2C_ADDR: int = 60

OLED_CTRL_BYTE_CMD_SINGLE: int = 128

OLED_CTRL_BYTE_CMD_STREAM: int = 0

OLED_CTRL_BYTE_DATA_STREAM: int = 64

OLED_CMD_SET_CONTRAST: int = 129

OLED_CMD_DISPLAY_RAM: int = 164

OLED_CMD_DISPLAY_ALLON: int = 165

OLED_CMD_DISPLAY_NORMAL: int = 166

OLED_CMD_DISPLAY_INVERTED: int = 167

OLED_CMD_DISPLAY_OFF: int = 174

OLED_CMD_DISPLAY_ON: int = 175

OLED_CMD_SET_MEMORY_ADDR_MODE: int = 32

OLED_CMD_SET_COLUMN_RANGE: int = 33

OLED_CMD_SET_PAGE_RANGE: int = 34

OLED_CMD_SET_DISPLAY_START_LINE: int = 64

OLED_CMD_SET_SEGMENT_REMAP: int = 161

OLED_CMD_SET_MUX_RATIO: int = 168

OLED_CMD_SET_COM_SCAN_MODE: int = 200

OLED_CMD_SET_DISPLAY_OFFSET: int = 211

OLED_CMD_SET_COM_PIN_MAP: int = 218

OLED_CMD_NOP: int = 227

OLED_CMD_SET_DISPLAY_CLK_DIV: int = 213

OLED_CMD_SET_PRECHARGE: int = 217

OLED_CMD_SET_VCOMH_DESELCT: int = 219

OLED_CMD_SET_CHARGE_PUMP: int = 141

OLED_SET_PAGE_ADDRESS: int = 176
