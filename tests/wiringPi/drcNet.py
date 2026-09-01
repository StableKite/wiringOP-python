import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.drc_net")

def test_drc_setup_net():
    _=m.drc_setup_net(1, 1, "x", "x", "x")
