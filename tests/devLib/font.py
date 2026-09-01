import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.font")

def test_variable_font_height():
    assert hasattr(m,"font_height")

def test_variable_font_width():
    assert hasattr(m,"font_width")

def test_variable_font():
    assert hasattr(m,"font")
