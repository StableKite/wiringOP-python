import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.mcp4802")

def test_mcp4802_setup():
    _=m.mcp4802_setup(1, 1)
