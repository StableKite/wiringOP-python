import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.mcp23016")

def test_mcp23016_setup():
    _=m.mcp23016_setup(1, 1)
