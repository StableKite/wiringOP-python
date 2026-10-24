import importlib

m = importlib.import_module("wiringop.wiring_pi.mcp3002")


def test_mcp3002_setup():
    _ = m.mcp3002_setup(1, 1)
