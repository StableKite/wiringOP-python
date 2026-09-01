import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.mcp3422")

def test_mcp3422_setup():
    _=m.mcp3422_setup(1, 1, 1, 1)

def test_constants_and_macros():
    assert hasattr(m,"MCP3422_SR_240")
    assert hasattr(m,"MCP3422_SR_60")
    assert hasattr(m,"MCP3422_SR_15")
    assert hasattr(m,"MCP3422_SR_3_75")
    assert hasattr(m,"MCP3422_GAIN_1")
    assert hasattr(m,"MCP3422_GAIN_2")
    assert hasattr(m,"MCP3422_GAIN_4")
    assert hasattr(m,"MCP3422_GAIN_8")
