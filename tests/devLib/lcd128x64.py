import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.lcd128x64")

def test_lcd128x64set_origin():
    _=m.lcd128x64set_origin(1, 1)

def test_lcd128x64set_orientation():
    _=m.lcd128x64set_orientation(1)

def test_lcd128x64orient_coordinates():
    assert m.lcd128x64orient_coordinates()==(1,2)

def test_lcd128x64_get_screen_size():
    assert m.lcd128x64_get_screen_size()==(128,64)

def test_lcd128x64point():
    _=m.lcd128x64point(1, 1, 1)

def test_lcd128x64line():
    _=m.lcd128x64line(1, 1, 1, 1, 1)

def test_lcd128x64line_to():
    _=m.lcd128x64line_to(1, 1, 1)

def test_lcd128x64rectangle():
    _=m.lcd128x64rectangle(1, 1, 1, 1, 1, 1)

def test_lcd128x64circle():
    _=m.lcd128x64circle(1, 1, 1, 1, 1)

def test_lcd128x64ellipse():
    _=m.lcd128x64ellipse(1, 1, 1, 1, 1, 1)

def test_lcd128x64putchar():
    _=m.lcd128x64putchar(1, 1, 1, 1, 1)

def test_lcd128x64puts():
    _=m.lcd128x64puts(1, 1, "x", 1, 1)

def test_lcd128x64update():
    _=m.lcd128x64update()

def test_lcd128x64clear():
    _=m.lcd128x64clear(1)

def test_lcd128x64setup():
    _=m.lcd128x64setup()
