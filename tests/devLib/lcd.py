import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.lcd")

def test_lcd_home():
    _=m.lcd_home(1)

def test_lcd_clear():
    _=m.lcd_clear(1)

def test_lcd_display():
    _=m.lcd_display(1, 1)

def test_lcd_cursor():
    _=m.lcd_cursor(1, 1)

def test_lcd_cursor_blink():
    _=m.lcd_cursor_blink(1, 1)

def test_lcd_send_command():
    _=m.lcd_send_command(1, 1)

def test_lcd_position():
    _=m.lcd_position(1, 1, 1)

def test_lcd_char_def():
    m.lcd_char_def(1,0,b"12345678")
    with pytest.raises(ValueError):m.lcd_char_def(1,0,b"x")

def test_lcd_putchar():
    _=m.lcd_putchar(1, 1)

def test_lcd_puts():
    _=m.lcd_puts(1, "x")

def test_lcd_printf():
    m.lcd_printf(1, "safe text")

def test_lcd_init():
    _=m.lcd_init(1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)

def test_constants_and_macros():
    assert hasattr(m,"MAX_LCDS")
