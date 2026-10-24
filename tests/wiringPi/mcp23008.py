import importlib

m = importlib.import_module("wiringop.wiring_pi.mcp23008")


def test_mcp23008_setup():
    _ = m.mcp23008_setup(1, 1)
