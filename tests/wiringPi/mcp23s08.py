import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.mcp23s08")

def test_mcp23s08_setup():
    _=m.mcp23s08_setup(1, 1, 1)
