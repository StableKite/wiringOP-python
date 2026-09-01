import importlib
import pytest

m=importlib.import_module("wiringop.dev_lib.pi_glow")

def test_pi_glow1():
    _=m.pi_glow1(1, 1, 1)

def test_pi_glow_leg():
    _=m.pi_glow_leg(1, 1)

def test_pi_glow_ring():
    _=m.pi_glow_ring(1, 1)

def test_pi_glow_setup():
    _=m.pi_glow_setup(1)

def test_constants_and_macros():
    assert hasattr(m,"PIGLOW_RED")
    assert hasattr(m,"PIGLOW_ORANGE")
    assert hasattr(m,"PIGLOW_YELLOW")
    assert hasattr(m,"PIGLOW_GREEN")
    assert hasattr(m,"PIGLOW_BLUE")
    assert hasattr(m,"PIGLOW_WHITE")
