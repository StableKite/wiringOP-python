import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.pcf8574")

def test_pcf8574_setup():
    _=m.pcf8574_setup(1, 1)
