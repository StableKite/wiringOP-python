import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.sr595")

def test_sr595_setup():
    _=m.sr595_setup(1, 1, 1, 1, 1)
