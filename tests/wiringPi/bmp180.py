import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.bmp180")

def test_bmp180_setup():
    _=m.bmp180_setup(1)
