import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.maxdetect")

def test_max_detect_read():
    assert m.max_detect_read(1)==(1,b"\x01\x02\x03\x04")

def test_read_rht03():
    assert m.read_rht03(1)==(1,234,567)
