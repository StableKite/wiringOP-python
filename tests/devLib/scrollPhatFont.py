import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.scroll_phat_font")

def test_variable_font_height():
    assert hasattr(m,"font_height")

def test_variable_scroll_phat_font():
    assert hasattr(m,"scroll_phat_font")
