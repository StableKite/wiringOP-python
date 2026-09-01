import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.sn3218")

def test_sn3218_setup():
    _=m.sn3218_setup(1)
