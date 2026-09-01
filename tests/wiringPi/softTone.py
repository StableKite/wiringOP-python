import importlib
import pytest

m=importlib.import_module("wiringop.wiring_pi.soft_tone")

def test_soft_tone_create():
    _=m.soft_tone_create(1)

def test_soft_tone_stop():
    _=m.soft_tone_stop(1)

def test_soft_tone_write():
    _=m.soft_tone_write(1, 1)
