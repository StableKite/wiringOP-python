import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.ds18b20")

def test_ds18b20_setup():
    _=m.ds18b20_setup(1, "x")
