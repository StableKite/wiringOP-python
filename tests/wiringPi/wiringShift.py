import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.wiring_shift")

def test_shift_in():
    _=m.shift_in(1, 1, 1)

def test_shift_out():
    _=m.shift_out(1, 1, 1, 1)

def test_constants_and_macros():
    assert hasattr(m,"LSBFIRST")
    assert hasattr(m,"MSBFIRST")
