import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.htu21d")

def test_htu21d_setup():
    _=m.htu21d_setup(1)
