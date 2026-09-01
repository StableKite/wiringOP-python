import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.pcf8591")

def test_pcf8591_setup():
    _=m.pcf8591_setup(1, 1)
