import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.max31855")

def test_max31855_setup():
    _=m.max31855_setup(1, 1)
