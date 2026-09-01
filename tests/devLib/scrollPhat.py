import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.scroll_phat")

def test_scroll_phat_point():
    _=m.scroll_phat_point(1, 1, 1)

def test_scroll_phat_line():
    _=m.scroll_phat_line(1, 1, 1, 1, 1)

def test_scroll_phat_line_to():
    _=m.scroll_phat_line_to(1, 1, 1)

def test_scroll_phat_rectangle():
    _=m.scroll_phat_rectangle(1, 1, 1, 1, 1, 1)

def test_scroll_phat_update():
    _=m.scroll_phat_update()

def test_scroll_phat_clear():
    _=m.scroll_phat_clear()

def test_scroll_phat_putchar():
    _=m.scroll_phat_putchar(1)

def test_scroll_phat_puts():
    _=m.scroll_phat_puts("x")

def test_scroll_phat_printf():
    m.scroll_phat_printf("safe text")

def test_scroll_phat_print_speed():
    _=m.scroll_phat_print_speed(1)

def test_scroll_phat_intensity():
    _=m.scroll_phat_intensity(1)

def test_scroll_phat_setup():
    _=m.scroll_phat_setup()
