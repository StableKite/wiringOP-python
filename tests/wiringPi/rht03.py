import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.rht03")

def test_rht03_setup():
    _=m.rht03_setup(1, 1)
