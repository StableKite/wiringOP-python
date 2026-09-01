import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.mcp23017")

def test_mcp23017_setup():
    _=m.mcp23017_setup(1, 1)
