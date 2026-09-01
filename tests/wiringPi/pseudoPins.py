import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.pseudo_pins")

def test_pseudo_pins_setup():
    _=m.pseudo_pins_setup(1)
