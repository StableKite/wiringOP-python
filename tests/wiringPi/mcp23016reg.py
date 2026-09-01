import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.mcp23016reg")

def test_constants_and_macros():
    assert hasattr(m,"MCP23016_GP0")
    assert hasattr(m,"MCP23016_GP1")
    assert hasattr(m,"MCP23016_OLAT0")
    assert hasattr(m,"MCP23016_OLAT1")
    assert hasattr(m,"MCP23016_IPOL0")
    assert hasattr(m,"MCP23016_IPOL1")
    assert hasattr(m,"MCP23016_IODIR0")
    assert hasattr(m,"MCP23016_IODIR1")
    assert hasattr(m,"MCP23016_INTCAP0")
    assert hasattr(m,"MCP23016_INTCAP1")
    assert hasattr(m,"MCP23016_IOCON0")
    assert hasattr(m,"MCP23016_IOCON1")
    assert hasattr(m,"IOCON_IARES")
    assert hasattr(m,"IOCON_INIT")
