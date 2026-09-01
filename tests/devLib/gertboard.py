import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.gertboard")

def test_gertboard_analog_write():
    _=m.gertboard_analog_write(1, 1)

def test_gertboard_analog_read():
    _=m.gertboard_analog_read(1)

def test_gertboard_spi_setup():
    _=m.gertboard_spi_setup()

def test_gertboard_analog_setup():
    _=m.gertboard_analog_setup(1)
