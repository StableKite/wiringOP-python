import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.max5322")

def test_max5322_setup():
    _=m.max5322_setup(1, 1)
