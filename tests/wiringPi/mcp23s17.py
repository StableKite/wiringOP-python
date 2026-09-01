import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.mcp23s17")

def test_mcp23s17_setup():
    _=m.mcp23s17_setup(1, 1, 1)
