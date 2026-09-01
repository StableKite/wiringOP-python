import importlib
import pytest

m=importlib.import_module("wiringop.version")

def test_constants_and_macros():
    assert hasattr(m,"VERSION")
    assert hasattr(m,"VERSION_MAJOR")
    assert hasattr(m,"VERSION_MINOR")
