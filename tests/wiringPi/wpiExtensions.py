import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.wpi_extensions")

def test_load_wpi_extension():
    m.load_wpi_extension("x", "x", 1)
