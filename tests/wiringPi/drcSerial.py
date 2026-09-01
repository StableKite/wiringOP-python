import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.drc_serial")

def test_drc_setup_serial():
    _=m.drc_setup_serial(1, 1, "x", 1)
