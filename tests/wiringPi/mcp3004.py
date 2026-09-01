import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.mcp3004")

def test_mcp3004_setup():
    _=m.mcp3004_setup(1, 1)
